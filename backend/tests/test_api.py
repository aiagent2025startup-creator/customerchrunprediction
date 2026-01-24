import pytest
from fastapi.testclient import TestClient
from backend.main import app
import time

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Test Data
valid_customer = {
    "Call_Failure": 8,
    "Complains": 0,
    "Subscription_Length": 38,
    "Charge_Amount": 0,
    "Seconds_of_Use": 4370,
    "Frequency_of_use": 71,
    "Frequency_of_SMS": 5,
    "Distinct_Called_Numbers": 17,
    "Age_Group": 3,
    "Tariff_Plan": 1,
    "Status": 1,
    "Age": 30,
    "Customer_Value": 197.64
}

high_risk_customer = {
    "Call_Failure": 20,
    "Complains": 1,
    "Subscription_Length": 2,
    "Charge_Amount": 0,
    "Seconds_of_Use": 100,
    "Frequency_of_use": 5,
    "Frequency_of_SMS": 0,
    "Distinct_Called_Numbers": 2,
    "Age_Group": 2,
    "Tariff_Plan": 1,
    "Status": 1,
    "Age": 25,
    "Customer_Value": 10.0
}

class TestRootEndpoints:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "model_name" in data
        assert "model_version" in data

class TestPredictionEndpoint:
    def test_valid_prediction(self, client):
        response = client.post("/predict", json=valid_customer)
        assert response.status_code == 200
        data = response.json()
        assert "churn_prediction" in data
        assert "risk_level" in data
        assert 0.0 <= data["churn_probability"] <= 1.0

    def test_invalid_age(self, client):
        invalid_data = valid_customer.copy()
        invalid_data["Age"] = 150  # Max is 120
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422

    def test_missing_field(self, client):
        invalid_data = valid_customer.copy()
        del invalid_data["Call_Failure"]
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422

class TestBatchPrediction:
    def test_batch_prediction(self, client):
        batch_data = {"customers": [valid_customer, high_risk_customer]}
        response = client.post("/predict/batch", json=batch_data)
        assert response.status_code == 200
        data = response.json()
        assert data["total_customers"] == 2
        assert len(data["predictions"]) == 2

    def test_empty_batch(self, client):
        response = client.post("/predict/batch", json={"customers": []})
        assert response.status_code == 422

    def test_max_batch(self, client):
        # Create 100 customers
        batch_data = {"customers": [valid_customer] * 100}
        response = client.post("/predict/batch", json=batch_data)
        assert response.status_code == 200
        assert response.json()["total_customers"] == 100

    def test_batch_prediction_csv(self, client):
        import io
        import pandas as pd
        
        # Create a sample CSV
        df = pd.DataFrame([valid_customer, high_risk_customer])
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        files = {"file": ("test.csv", csv_buffer, "text/csv")}
        response = client.post("/predict/batch/csv", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_customers"] == 2
        assert len(data["predictions"]) == 2
        assert "processing_time_ms" in data

class TestModelInfo:
    def test_model_info(self, client):
        response = client.get("/model/info")
        assert response.status_code == 200
        data = response.json()
        assert data["model_type"] == "LightGBM"
        assert data["feature_count"] >= 13

class TestPerformance:
    def test_latency(self, client):
        start = time.time()
        response = client.post("/predict", json=valid_customer)
        end = time.time()
        assert response.status_code == 200
        latency = (end - start) * 1000
        # Allow some buffer for test environment overhead
        assert latency < 200

    def test_concurrent_requests(self, client):
        # TestClient is synchronous, so we can't truly test concurrency here without threads/async
        # But we can verify multiple sequential requests work fine
        for _ in range(50):
            response = client.post("/predict", json=valid_customer)
            assert response.status_code == 200

class TestDataValidation:
    def test_complains_validation(self, client):
        invalid_data = valid_customer.copy()
        invalid_data["Complains"] = 2  # Only 0 or 1 allowed
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422

    def test_age_group_validation(self, client):
        invalid_data = valid_customer.copy()
        invalid_data["Age_Group"] = 6  # 1-5 allowed
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422
