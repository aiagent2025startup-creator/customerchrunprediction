# ⏱️ Quickstart Guide

Get ChurnGuard AI up and running in less than 5 minutes.

## Step 1: Clone & Navigate
```bash
git clone https://github.com/yourusername/customerchrunprediction.git
cd customerchrunprediction
```

## Step 2: Virtual Environment
We recommend using a virtual environment to avoid dependency conflicts.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Packages
```bash
pip install -r backend/requirements.txt
```

## Step 4: Launch
```bash
uvicorn backend.main:app --port 8001 --reload
```

## Step 5: Explore
- **Dashboard**: [http://localhost:8001](http://localhost:8001)
- **API Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)

---
**Note**: Ensure you have the `churn_model.pkl` and other model artifacts in the `backend/` folder before starting.
