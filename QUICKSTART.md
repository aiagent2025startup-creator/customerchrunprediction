# ⚡ Churn Prediction API - Quick Start Guide

Follow these steps to get the API up and running in 5 minutes.

## 1. Setup (30 sec)

Ensure you have the following files:
```
churn-week1/
├── train.py
├── docker-compose.yml
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
└── docs/
```

## 2. Train Model (2 min)

If you haven't trained the model yet:

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run training script
python train.py
```
**Expected Output:**
- `✅ Target accuracy achieved!`
- Artifacts created in `backend/`: `churn_model.pkl`, `feature_names.pkl`, `model_metadata.pkl`

## 3. Launch API (60 sec)

Deploy using Docker (recommended):

```bash
docker-compose up -d
```

Verify it's running:
```bash
curl http://localhost:8000/health
```

## 4. Test API (30 sec)

Open your browser to the Swagger UI:
[http://localhost:8000/docs](http://localhost:8000/docs)

Or run a quick test:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Call_Failure": 8, "Complains": 0, "Subscription_Length": 38,
    "Charge_Amount": 0, "Seconds_of_Use": 4370, "Frequency_of_use": 71,
    "Frequency_of_SMS": 5, "Distinct_Called_Numbers": 17, "Age_Group": 3,
    "Tariff_Plan": 1, "Status": 1, "Age": 30, "Customer_Value": 197.64
  }'
```

## 5. Run Tests (1 min)

Validate the system:
```bash
pytest backend/tests/test_api.py -v
```
**Expected Result:** All tests passed (100% coverage).

## ✅ Success Checklist

- [ ] Model trained with >96% accuracy
- [ ] Docker container running
- [ ] Health check returns 200
- [ ] Prediction endpoint working
- [ ] All tests passing

## 🆘 Troubleshooting

- **Model not loaded?** Ensure `train.py` was run and artifacts exist in `backend/`.
- **Port busy?** Check if port 8000 is used by another app.
- **Docker error?** Run `docker-compose logs` to see details.
