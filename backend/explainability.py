import joblib
import pandas as pd
import numpy as np
import shap
import logging

logger = logging.getLogger(__name__)

class ExplainerService:
    def __init__(self, explainer_path='backend/shap_explainer.pkl'):
        self.explainer = None
        try:
            self.explainer = joblib.load(explainer_path)
            logger.info("✅ SHAP explainer loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Error loading SHAP explainer: {e}")

    def get_explanation(self, data: pd.DataFrame, top_k=3):
        """
        Generate SHAP values for a single instance and return top k features.
        """
        if self.explainer is None:
            return []

        try:
            # Calculate SHAP values
            # TreeExplainer for LightGBM returns matrix [samples, features]
            # For binary classification, it might return [samples, features] (log odds for class 1)
            # or [samples, features, 2] depending on version/model.
            # LightGBM binary usually returns just for class 1.
            
            shap_values = self.explainer.shap_values(data)
            
            # Handle different return shapes
            if isinstance(shap_values, list):
                # Multiclass or binary with 2 outputs
                # For binary, usually index 1 is the positive class
                sv = shap_values[1][0]
            elif len(shap_values.shape) == 2:
                sv = shap_values[0]
            else:
                sv = shap_values[0] # Fallback

            feature_names = data.columns.tolist()
            
            # Create list of (feature, impact)
            impacts = []
            for name, value in zip(feature_names, sv):
                impacts.append({
                    "feature": name,
                    "impact": float(value),
                    "abs_impact": abs(value)
                })
            
            # Sort by absolute impact
            impacts.sort(key=lambda x: x['abs_impact'], reverse=True)
            
            # Return top k
            return [
                {"feature": item["feature"], "impact": item["impact"]}
                for item in impacts[:top_k]
            ]
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return []

# Singleton instance
_service = None

def get_explainer_service():
    global _service
    if _service is None:
        _service = ExplainerService()
    return _service
