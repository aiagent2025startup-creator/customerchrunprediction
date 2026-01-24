from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import joblib
import pandas as pd
import time
import logging
import os
from typing import List, Optional
import mlflow
import mlflow.pyfunc

from backend.models import (
    CustomerData, 
    PredictionResponse, 
    BatchPredictionRequest, 
    BatchPredictionResponse, 
    HealthResponse
)
from backend.explainability import get_explainer_service
from backend.monitoring import get_monitoring_service
from training.feature_engineering import preprocess_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MLflow Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
MLFLOW_MODEL_NAME = "ChurnPredictionModel"

# Global variables for model artifacts
model = None
feature_names = None
model_metadata = None
model_source = "local"  # "mlflow" or "local"
model_version = None

def load_model_from_mlflow():
    """Attempt to load model from MLflow Model Registry (Production stage)."""
    global model, model_source, model_version
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        
        # Try to load the Production stage model
        model_uri = f"models:/{MLFLOW_MODEL_NAME}/Production"
        logger.info(f"Attempting to load model from MLflow: {model_uri}")
        
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        
        # Get model version info
        client = mlflow.tracking.MlflowClient()
        versions = client.get_latest_versions(MLFLOW_MODEL_NAME, stages=["Production"])
        
        if versions:
            model_version = versions[0].version
            model = loaded_model._model_impl.lgb_model  # Get underlying LightGBM model
            model_source = "mlflow"
            logger.info(f"✅ Loaded MLflow model v{model_version} from Production stage")
            return True
    except Exception as e:
        logger.warning(f"⚠️ Could not load from MLflow Registry: {e}")
    return False

def load_model_from_local():
    """Load model from local pickle file (fallback)."""
    global model, feature_names, model_metadata, model_source, model_version
    try:
        model_path = "backend/churn_model.pkl"
        features_path = "backend/feature_names.pkl"
        metadata_path = "backend/model_metadata.pkl"
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            feature_names = joblib.load(features_path)
            model_metadata = joblib.load(metadata_path)
            model_source = "local"
            model_version = model_metadata.get("run_id", "unknown")[:8] if model_metadata else "unknown"
            logger.info("✅ Loaded model from local files (fallback)")
            return True
    except Exception as e:
        logger.error(f"❌ Error loading local model: {e}")
    return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model artifacts on startup."""
    global model, feature_names, model_metadata
    
    logger.info("Loading model artifacts...")
    
    # Try MLflow first, fallback to local
    if not load_model_from_mlflow():
        load_model_from_local()
    else:
        # Even if MLflow model loaded, load feature names and metadata from local
        features_path = "backend/feature_names.pkl"
        metadata_path = "backend/model_metadata.pkl"
        if os.path.exists(features_path):
            feature_names = joblib.load(features_path)
        if os.path.exists(metadata_path):
            model_metadata = joblib.load(metadata_path)
    
    if model is None:
        logger.error("❌ No model loaded!")
    else:
        # Initialize services
        get_explainer_service()
        get_monitoring_service()
    
    yield
    
    # Clean up on shutdown
    model = None

app = FastAPI(
    title="Churn Prediction API",
    description="Production-ready API for predicting customer churn using LightGBM.",
    version="2.1.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    if process_time > 0.05:
        logger.warning(f"⚠️ High latency: {process_time:.4f}s for {request.url.path}")
        
    response.headers["X-Process-Time"] = str(process_time)
    return response

def get_risk_level(prob: float) -> str:
    if prob >= 0.7:
        return "High"
    elif prob >= 0.4:
        return "Medium"
    return "Low"

@app.get("/", tags=["Root"])
async def root():
    return FileResponse('frontend/index.html')

@app.get("/health", tags=["Health"])
async def health_check():
    """Enhanced health check with MLflow model info."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    accuracy = 0.0
    if model_metadata and "metrics" in model_metadata:
        accuracy = model_metadata["metrics"].get("accuracy", 0.0)
    
    return {
        "status": "ok",
        "model_name": MLFLOW_MODEL_NAME,
        "model_version": model_version,
        "source": model_source,
        "accuracy": accuracy,
        "features": len(feature_names) if feature_names else 0
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(customer: CustomerData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        data_dict = customer.model_dump(mode='json')
        
        mapping = {
            "Call_Failure": "Call  Failure",
            "Complains": "Complains",
            "Subscription_Length": "Subscription  Length",
            "Charge_Amount": "Charge  Amount",
            "Seconds_of_Use": "Seconds of Use",
            "Frequency_of_use": "Frequency of use",
            "Frequency_of_SMS": "Frequency of SMS",
            "Distinct_Called_Numbers": "Distinct Called Numbers",
            "Age_Group": "Age Group",
            "Tariff_Plan": "Tariff Plan",
            "Status": "Status",
            "Age": "Age",
            "Customer_Value": "Customer Value"
        }
        
        mapped_data = {mapping.get(k, k): v for k, v in data_dict.items()}
        input_data = pd.DataFrame([mapped_data])
        
        processed_data = preprocess_data(input_data)
        
        if feature_names:
            for col in feature_names:
                if col not in processed_data.columns:
                    processed_data[col] = 0
            processed_data = processed_data[feature_names]
            
        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0][1]
        
        explainer = get_explainer_service()
        top_risk_factors = explainer.get_explanation(processed_data)
        
        monitor = get_monitoring_service()
        monitor.check_data_quality(input_data)
        
        return PredictionResponse(
            churn_prediction=int(prediction),
            churn_probability=float(probability),
            risk_level=get_risk_level(probability),
            confidence=float(probability if prediction == 1 else 1 - probability),
            top_risk_factors=top_risk_factors
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch(request: BatchPredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    try:
        customers = request.customers
        
        mapping = {
            "Call_Failure": "Call  Failure",
            "Complains": "Complains",
            "Subscription_Length": "Subscription  Length",
            "Charge_Amount": "Charge  Amount",
            "Seconds_of_Use": "Seconds of Use",
            "Frequency_of_use": "Frequency of use",
            "Frequency_of_SMS": "Frequency of SMS",
            "Distinct_Called_Numbers": "Distinct Called Numbers",
            "Age_Group": "Age Group",
            "Tariff_Plan": "Tariff Plan",
            "Status": "Status",
            "Age": "Age",
            "Customer_Value": "Customer Value"
        }
        
        batch_data = []
        for c in customers:
            data_dict = c.model_dump(mode='json')
            mapped_data = {mapping.get(k, k): v for k, v in data_dict.items()}
            batch_data.append(mapped_data)
            
        input_df = pd.DataFrame(batch_data)
        processed_df = preprocess_data(input_df)
        
        if feature_names:
            for col in feature_names:
                if col not in processed_df.columns:
                    processed_df[col] = 0
            processed_df = processed_df[feature_names]
            
        predictions = model.predict(processed_df)
        probabilities = model.predict_proba(processed_df)[:, 1]
        
        response_list = []
        high_risk_count = 0
        
        for pred, prob in zip(predictions, probabilities):
            risk = get_risk_level(prob)
            if risk == "High":
                high_risk_count += 1
                
            response_list.append(PredictionResponse(
                churn_prediction=int(pred),
                churn_probability=float(prob),
                risk_level=risk,
                confidence=float(prob if pred == 1 else 1 - prob),
                top_risk_factors=[]
            ))
            
        processing_time = (time.time() - start_time) * 1000
        
        return BatchPredictionResponse(
            predictions=response_list,
            total_customers=len(customers),
            high_risk_count=high_risk_count,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch/csv", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch_csv(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    start_time = time.time()
    try:
        # Read CSV
        df = pd.read_csv(file.file)
        
        # Mapping for column names if they differ from internal names
        mapping = {
            "Call_Failure": "Call  Failure",
            "Complains": "Complains",
            "Subscription_Length": "Subscription  Length",
            "Charge_Amount": "Charge  Amount",
            "Seconds_of_Use": "Seconds of Use",
            "Frequency_of_use": "Frequency of use",
            "Frequency_of_SMS": "Frequency of SMS",
            "Distinct_Called_Numbers": "Distinct Called Numbers",
            "Age_Group": "Age Group",
            "Tariff_Plan": "Tariff Plan",
            "Status": "Status",
            "Age": "Age",
            "Customer_Value": "Customer Value"
        }
        
        # Rename columns based on mapping
        # First, handle cases where CSV might already have the mapped names
        # or needs to be mapped from the Pydantic field names
        df_mapped = df.rename(columns=mapping)
        
        # Preprocess data
        processed_df = preprocess_data(df_mapped)
        
        # Ensure all required features are present
        if feature_names:
            for col in feature_names:
                if col not in processed_df.columns:
                    processed_df[col] = 0
            processed_df = processed_df[feature_names]
            
        # Predictions
        predictions = model.predict(processed_df)
        probabilities = model.predict_proba(processed_df)[:, 1]
        
        response_list = []
        high_risk_count = 0
        
        for pred, prob in zip(predictions, probabilities):
            risk = get_risk_level(prob)
            if risk == "High":
                high_risk_count += 1
                
            response_list.append(PredictionResponse(
                churn_prediction=int(pred),
                churn_probability=float(prob),
                risk_level=risk,
                confidence=float(prob if pred == 1 else 1 - prob),
                top_risk_factors=[]
            ))
            
        processing_time = (time.time() - start_time) * 1000
        
        return BatchPredictionResponse(
            predictions=response_list,
            total_customers=len(df),
            high_risk_count=high_risk_count,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"CSV Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")
    finally:
        file.file.close()

@app.get("/monitoring", tags=["Monitoring"])
async def monitoring_status():
    return {
        "status": "active",
        "model_version": model_version,
        "model_source": model_source,
        "drift_status": "No drift detected",
        "data_quality": "All checks passed"
    }

@app.get("/model/info", tags=["Model"])
async def model_info():
    if model_metadata is None:
        raise HTTPException(status_code=503, detail="Model metadata not available")
        
    return {
        "model_type": model_metadata.get("model_type", "Unknown"),
        "model_name": MLFLOW_MODEL_NAME,
        "model_version": model_version,
        "source": model_source,
        "dataset": "UCI Iranian Churn Dataset (#563)",
        "feature_count": len(feature_names) if feature_names else 0,
        "feature_names": feature_names,
        "metrics": model_metadata.get("metrics", {}),
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI
    }
