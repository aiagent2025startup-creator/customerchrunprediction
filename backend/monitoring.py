import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import joblib
import logging

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self, reference_data_path='backend/feature_names.pkl'):
        # In a real system, we'd load the actual training data distribution
        # For this simplified version, we'll assume we have access to some stats
        # or we just check for schema validity and basic range checks.
        # To do drift properly, we need the training data.
        # Let's try to load the training data if available, or just skip drift if not.
        self.reference_data = None
        try:
            # Ideally we would save a sample of training data
            pass 
        except Exception:
            pass

    def check_drift(self, current_data: pd.DataFrame, reference_data: pd.DataFrame = None):
        """
        Check for prediction drift using KS test.
        """
        drift_report = {}
        drift_detected = False
        
        if reference_data is None:
            return {"status": "unknown", "details": "No reference data"}

        for col in current_data.columns:
            if col in reference_data.columns:
                # KS Test
                stat, p_value = ks_2samp(current_data[col], reference_data[col])
                if p_value < 0.05: # Drift detected
                    drift_detected = True
                    drift_report[col] = {
                        "drift_detected": True,
                        "p_value": float(p_value)
                    }
        
        return {
            "drift_detected": drift_detected,
            "details": drift_report
        }

    def check_data_quality(self, data: pd.DataFrame):
        """
        Basic data quality checks.
        """
        issues = []
        
        # Check for missing values
        if data.isnull().any().any():
            issues.append("Missing values detected")
            
        # Check for negative values in strictly positive columns
        positive_cols = ['Seconds of Use', 'Subscription  Length', 'Age']
        for col in positive_cols:
            if col in data.columns and (data[col] < 0).any():
                issues.append(f"Negative values in {col}")
                
        return {
            "status": "passed" if not issues else "warning",
            "issues": issues
        }

# Singleton
_monitor = None

def get_monitoring_service():
    global _monitor
    if _monitor is None:
        _monitor = MonitoringService()
    return _monitor
