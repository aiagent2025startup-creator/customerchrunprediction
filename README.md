# ChurnGuard AI - Production Customer Intelligence System

ChurnGuard AI is an end-to-end, high-performance customer churn prediction platform. It leverages **LightGBM** and **FastAPI** to provide real-time risk assessments, actionable insights, and a comprehensive Business Intelligence dashboard with interactive visualizations.

![System Showcase](https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge) ![Tech-FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi) ![Tech-JS](https://img.shields.io/badge/Frontend-Vanilla%20JS-F7DF1E?style=for-the-badge&logo=javascript)

## 🚀 Key Features

- **Predictive Intelligence**: State-of-the-art LightGBM model trained on behavioral datasets.
- **Explainable AI (XAI)**: Integrated SHAP analysis to explain *why* a customer is at risk.
- **Premium UI**: Glassmorphism interface with smooth transitions and layout stability.
- **Production-ready API**: Optimized endpoints with sub-100ms inference times.

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, FastAPI, Pydantic v2
- **ML Engine**: LightGBM, Scikit-learn, Pandas, SHAP
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6+)
- **Charts**: Chart.js 4.x
- **Monitoring**: MLflow (Tracking & Registry)

## 📂 Folder Structure

```text
customerchrunprediction/
├── backend/                # FastAPI Application & Logic
│   ├── main.py             # Entry point & Static serving
│   ├── models.py           # Pydantic Schemas (v2 compliant)
│   ├── explainability.py   # SHAP explainers
│   └── monitoring.py       # Data drift metrics
├── frontend/               # Dashboard UI
│   ├── index.html          # Main application structure
│   ├── script.js           # Chart lifecycle & state logic
│   └── style.css           # Premium styling & layouts
├── training/               # Model Training & Engineering
│   └── feature_engineering.py
├── QUICKSTART.md           # Beginner setup guide
└── README.md               # Professional documentation
```

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.9+
- Git

### 2. Environment Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd customerchrunprediction

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
.\venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Running the Application
The backend serves both the API and the frontend dashboard.

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```
Access the application at: **[http://localhost:8001](http://localhost:8001)**

## 🔌 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/health` | `GET` | System & Model status |
| `/predict` | `POST` | Single churn risk analysis |
| `/analytics` | `GET` | Dashboard visualization data |
| `/model/info` | `GET` | Model features & metadata |

## 🛠️ Troubleshooting

- **Port Conflict**: If port 8001 is used, run with `--port <new_port>`.
- **Model Missing**: Ensure `.pkl` files are present in the `backend/` directory.
- **Chart Resizing**: If charts look small, ensure the window is resized once or tab is switched.

## 🚀 Future Improvements

- [ ] Automated CI/CD pipeline for model redeployment.
- [ ] Multi-tenant support for different customer segments.
- [ ] Real-time data stream integration (Kafka/WebSocket).

## 👤 Author
**Senior Development Team**
*Technical Leader: Antigravity AI*
