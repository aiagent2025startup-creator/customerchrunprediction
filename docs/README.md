# 🚀 Churn Prediction API

A production-ready FastAPI system for predicting customer churn using LightGBM on the UCI Iranian Churn dataset.

## 📋 Overview

- **Accuracy**: 96%+ (Validated via 10-fold CV)
- **Latency**: <50ms per request
- **Throughput**: 1000+ req/sec
- **Deployment**: Dockerized with Uvicorn workers

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Deploy with Docker (Recommended)
```bash
docker-compose up -d
```
Verify deployment:
```bash
curl http://localhost:8000/health
```

### Local Development
1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn backend.main:app --reload
   ```

## 🔌 API Endpoints

Full documentation available at `http://localhost:8000/docs` (Swagger UI).

### 1. Health Check
`GET /health`
Returns model status and accuracy metrics.

### 2. Single Prediction
`POST /predict`
Predict churn for a single customer.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "churn_prediction": 0,
  "churn_probability": 0.042,
  "risk_level": "Low",
  "confidence": 0.958
}
```

### 3. Batch Prediction
`POST /predict/batch`
Predict churn for multiple customers (max 100).

### 4. Model Info
`GET /model/info`
Returns metadata about the trained model and dataset.

## 📊 Features

| Feature | Type | Description |
|---------|------|-------------|
| Call_Failure | int | Number of call failures |
| Complains | int (0/1) | Customer complained |
| Subscription_Length | float | Months subscribed |
| Charge_Amount | int (0-9) | Charge category |
| Seconds_of_Use | float | Usage seconds |
| Frequency_of_use | float | Usage frequency |
| Frequency_of_SMS | float | SMS frequency |
| Distinct_Called_Numbers | int | Unique numbers called |
| Age_Group | int (1-5) | Age category |
| Tariff_Plan | int (1/2) | Plan type |
| Status | int (1/2) | Account status |
| Age | int | Customer age |
| Customer_Value | float | Customer value score |

## 🧪 Testing

Run the test suite:
```bash
pytest backend/tests/test_api.py -v
```

## 🐳 Production Considerations

- **Security**: Add API Key authentication or OAuth2 for protected endpoints.
- **Monitoring**: Integrate Prometheus/Grafana for real-time metrics.
- **Scaling**: Adjust `WORKERS` in `docker-compose.yml` based on CPU cores.

## 🤖 Model Details

- **Algorithm**: LightGBM Classifier
- **Dataset**: UCI Iranian Churn Dataset (#563)
- **Training**: 80/20 split, 10-fold Stratified CV
- **Performance**: ~96% Accuracy
