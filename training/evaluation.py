from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    precision_recall_curve, f1_score, accuracy_score
)
import numpy as np
import mlflow

def evaluate_model(model, X_test, y_test, threshold=0.5):
    """
    Comprehensive model evaluation.
    """
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    f1 = f1_score(y_test, y_pred)
    
    print(f"📊 Accuracy: {acc:.4f}")
    print(f"📊 ROC-AUC: {roc_auc:.4f}")
    print(f"📊 F1 Score: {f1:.4f}")
    print("\n📝 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n🧱 Confusion Matrix:")
    print(cm)
    
    # Log metrics to MLflow
    mlflow.log_metric("test_accuracy", acc)
    mlflow.log_metric("test_roc_auc", roc_auc)
    mlflow.log_metric("test_f1", f1)
    
    return {
        "accuracy": acc,
        "roc_auc": roc_auc,
        "f1": f1,
        "confusion_matrix": cm.tolist()
    }

def find_optimal_threshold(model, X_test, y_test):
    """
    Find the threshold that maximizes F1 score.
    """
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_pred_proba)
    
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx]
    
    print(f"🎯 Optimal Threshold (max F1): {best_threshold:.4f}")
    return best_threshold
