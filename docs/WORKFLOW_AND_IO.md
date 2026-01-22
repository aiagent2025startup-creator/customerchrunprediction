# Project Workflow & API Specification

## 🔄 Project Workflow

This document outlines the end-to-end lifecycle of the Churn Prediction system.

### 1. Model Training Phase
**Goal:** Train a machine learning model on the Iranian Churn Dataset.
- **Script:** `train.py`
- **Process:**
    1.  **Fetch Data:** Downloads dataset (ID: 563) from UCI Repository.
    2.  **Preprocess:** Splits data into features/targets and train/test sets (80/20 split).
    3.  **Train:** Fits a **LightGBM Classifier**.
    4.  **Validate:** Performs 10-fold cross-validation to ensure >96% accuracy.
    5.  **Save Artifacts:** Saves the following to `backend/`:
        - `churn_model.pkl` (Model)
        - `feature_names.pkl` (Feature list)
        - `model_metadata.pkl` (Metrics)

### 2. API Startup Phase
**Goal:** Initialize the FastAPI server.
- **Entry Point:** `backend/main.py`
- **Process:**
    1.  **Lifespan Event:** On startup, loads the `.pkl` artifacts into memory.
    2.  **Health Check:** Verifies model is loaded via `GET /health`.

### 3. Prediction Phase
**Goal:** Generate churn predictions for users.
- **Endpoint:** `POST /predict`
- **Process:**
    1.  **Receive Data:** Accepts JSON payload with customer details.
    2.  **Validate:** Pydantic ensures data types and ranges are correct.
    3.  **Map:** Maps input fields to model-specific feature names.
    4.  **Infer:** Model calculates churn probability.
    5.  **Respond:** Returns prediction (0/1), probability, and risk level.

### 4. Frontend Interaction
**Goal:** User interface for predictions.
- **Location:** `frontend/` (served at `/`)
- **Process:**
    1.  User fills HTML form.
    2.  JavaScript sends data to `/predict`.
    3.  Result is displayed on screen.

---

## 🔌 API Input & Output Specification

### 📥 Input (Request Body)
**Endpoint:** `POST /predict`

| Field Name | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `Call_Failure` | `int` | `ge=0` | Number of call failures. |
| `Complains` | `int` | `0` or `1` | 0: No complaint, 1: Complaint. |
| `Subscription_Length` | `float` | `ge=0` | Months of subscription. |
| `Charge_Amount` | `int` | `0` to `9` | Ordinal charge category. |
| `Seconds_of_Use` | `float` | `ge=0` | Total usage seconds. |
| `Frequency_of_use` | `float` | `ge=0` | Total number of calls. |
| `Frequency_of_SMS` | `float` | `ge=0` | Total SMS count. |
| `Distinct_Called_Numbers` | `int` | `ge=0` | Unique numbers called. |
| `Age_Group` | `int` | `1` to `5` | Age category. |
| `Tariff_Plan` | `int` | `1` or `2` | 1: Pay as you go, 2: Contractual. |
| `Status` | `int` | `1` or `2` | 1: Active, 2: Non-active. |
| `Age` | `int` | `0` to `120` | Customer age. |
| `Customer_Value` | `float` | `ge=0` | Calculated customer value. |

### 📤 Output (Response Body)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `churn_prediction` | `int` | **0**: Non-churn, **1**: Churn. |
| `churn_probability` | `float` | Probability score (0.0 - 1.0). |
| `risk_level` | `string` | `Low`, `Medium`, or `High`. |
| `confidence` | `float` | Model confidence score (0.0 - 1.0). |
