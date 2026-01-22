import pandas as pd
import numpy as np
import joblib
import os
import mlflow
import mlflow.lightgbm
import shap
from ucimlrepo import fetch_ucirepo
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

from training.feature_engineering import preprocess_data
from training.tuning import optimize_hyperparameters
from training.evaluation import evaluate_model, find_optimal_threshold

# MLflow Configuration
MLFLOW_EXPERIMENT_NAME = "churn_prediction_lightgbm"
MLFLOW_MODEL_NAME = "ChurnPredictionModel"

def train_model():
    # Set up MLflow
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(f"🚀 MLflow Run ID: {run_id}")
        
        print("📦 Fetching UCI Iranian Churn dataset...")
        iranian_churn = fetch_ucirepo(id=563)
        
        X = iranian_churn.data.features
        y = iranian_churn.data.targets
        
        if isinstance(y, pd.DataFrame):
            y = y.iloc[:, 0]

        dataset_size = X.shape[0]
        print(f"✅ Dataset loaded: {dataset_size} rows, {X.shape[1]} features")
        
        # Log dataset info
        mlflow.log_param("dataset_size", dataset_size)
        mlflow.log_param("original_features", X.shape[1])
        
        # 1. Feature Engineering
        print("🛠️ Applying feature engineering...")
        X_processed = preprocess_data(X)
        print(f"✅ Features processed: {X_processed.shape[1]} features")
        mlflow.log_param("processed_features", X_processed.shape[1])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.2, random_state=42, stratify=y
        )
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        
        # 2. Hyperparameter Tuning
        print("🔍 Optimizing hyperparameters with Optuna...")
        best_params = optimize_hyperparameters(X_train, y_train, n_trials=20)
        mlflow.log_params(best_params)
        
        # 3. Train Final Model
        print("🏋️ Training final model...")
        model = LGBMClassifier(**best_params)
        model.fit(X_train, y_train)
        
        # 4. Evaluation
        print("📊 Evaluating model...")
        best_threshold = find_optimal_threshold(model, X_test, y_test)
        mlflow.log_param("optimal_threshold", best_threshold)
        
        metrics = evaluate_model(model, X_test, y_test, threshold=best_threshold)
        
        # Log additional metrics explicitly
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("roc_auc", metrics["roc_auc"])
        mlflow.log_metric("f1_score", metrics["f1"])
        
        # 5. Explainability (SHAP)
        print("🧠 Generating SHAP explainer...")
        explainer = shap.TreeExplainer(model)
        
        # 6. Save Local Artifacts (fallback)
        print("💾 Saving local artifacts to backend/...")
        os.makedirs('backend', exist_ok=True)
        
        joblib.dump(model, 'backend/churn_model.pkl')
        joblib.dump(X_processed.columns.tolist(), 'backend/feature_names.pkl')
        joblib.dump(explainer, 'backend/shap_explainer.pkl')
        
        metadata = {
            'metrics': metrics,
            'best_params': best_params,
            'optimal_threshold': best_threshold,
            'feature_count': len(X_processed.columns),
            'model_type': 'LightGBM',
            'run_id': run_id
        }
        joblib.dump(metadata, 'backend/model_metadata.pkl')
        
        # 7. Log artifacts to MLflow
        mlflow.log_artifact('backend/churn_model.pkl')
        mlflow.log_artifact('backend/feature_names.pkl')
        mlflow.log_artifact('backend/shap_explainer.pkl')
        mlflow.log_artifact('backend/model_metadata.pkl')
        
        # 8. Register Model in MLflow Model Registry
        print("📝 Registering model in MLflow Model Registry...")
        model_uri = f"runs:/{run_id}/model"
        
        # Log the LightGBM model with MLflow
        mlflow.lightgbm.log_model(
            model, 
            artifact_path="model",
            registered_model_name=MLFLOW_MODEL_NAME
        )
        
        print(f"✅ Model registered as '{MLFLOW_MODEL_NAME}'")
        print(f"✅ MLflow Run ID: {run_id}")
        print("✅ All artifacts saved successfully.")
        print("\n📋 Next Steps:")
        print("   1. Start MLflow UI: mlflow ui --port 5000")
        print(f"   2. Promote model to 'Production' stage in the UI")
        print("   3. Restart FastAPI to load the production model")

if __name__ == "__main__":
    train_model()
