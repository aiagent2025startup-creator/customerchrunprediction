# Customer Churn Prediction System

An end-to-end Machine Learning project that predicts customer churn using **LightGBM**, served via **FastAPI**, and tracked using **MLflow**. The entire application is containerized with **Docker** for easy deployment.

## 🚀 Project Overview
This project provides a complete pipeline from model training to production deployment. It includes a web-based dashboard where users can input customer details and receive real-time churn risk assessments.

## 🛠️ Technologies Used
- **Backend:** FastAPI (Python)
- **Machine Learning:** LightGBM, Scikit-learn, Pandas
- **MLOps:** MLflow (Tracking & Model Registry)
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Containerization:** Docker, Docker Compose

## 📂 Folder Structure
```text
.
├── backend/            # FastAPI application & Model logic
├── frontend/           # Web interface files
├── training/           # Data preprocessing & Training scripts
├── mlruns/             # MLflow tracking data
├── docker-compose.yml  # Docker orchestration
├── train.py            # Main training script
└── requirements.txt    # Python dependencies
```

## 📋 Prerequisites
Ensure you have the following installed:
- Python 3.9+
- Docker & Docker Compose

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/aiagent2025startup-creator/customercruhnped.git
cd customercruhnped
```

### 2. Local Setup (Without Docker)
If you wish to run components individually:

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Start MLflow Server:**
```bash
mlflow ui --host 0.0.0.0 --port 5000
```

**Train the Model:**
```bash
python train.py
```

**Run FastAPI Backend:**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 3. Docker Setup (Recommended)
To run the entire system (MLflow + API + Frontend) with one command:
```bash
docker-compose up -d --build
```

## 🔗 Access URLs
- **Frontend:** [http://localhost:8000](http://localhost:8000)
- **API Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **MLflow UI:** [http://localhost:5000](http://localhost:5000)

## 🧪 API Usage Example
You can test the prediction endpoint using `curl`:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "Call_Failure": 5,
       "Complains": 0,
       "Subscription_Length": 12,
       "Charge_Amount": 2,
       "Seconds_of_Use": 1000,
       "Frequency_of_use": 20,
       "Frequency_of_SMS": 10,
       "Distinct_Called_Numbers": 5,
       "Age_Group": 2,
       "Tariff_Plan": 1,
       "Status": 1,
       "Age": 25,
       "Customer_Value": 50.5
     }'
```

## ⚠️ Common Errors & Fixes
- **Port 5000/8000 already in use:** Stop any existing services running on these ports or change the mapping in `docker-compose.yml`.
- **Model Not Found:** Ensure you run `train.py` at least once so that MLflow has a registered model to serve.
- **Docker Permissions:** On Linux, you might need to run docker commands with `sudo`.

## 🎓 Conclusion
This project serves as a robust template for deploying machine learning models in a production environment using modern MLOps practices.
# customerchrunprediction
