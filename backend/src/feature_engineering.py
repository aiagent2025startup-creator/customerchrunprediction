import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, config):
        self.config = config
        self.scaler = None
        self.imputer = None
        self.feature_names_in_ = None
        self.feature_names_out_ = None
        
    def fit(self, X, y=None):
        logger.info("🛠️ Fitting FeatureEngineer...")
        self.feature_names_in_ = X.columns.tolist()
        
        # Handle missing values
        self.imputer = SimpleImputer(strategy='mean')
        self.imputer.fit(X)
        
        # Scaling
        scaling_type = self.config.get('feature_engineering', {}).get('scaling', 'standard')
        if scaling_type == 'standard':
            self.scaler = StandardScaler()
        elif scaling_type == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            self.scaler = None
            
        if self.scaler:
            # We need to fit scaler on transformed data (after imputation and feature creation)
            # But for simplicity in this custom class, we'll fit it on the base features first
            # Or better, we fit it in transform? No, fit must be done here.
            # Actually, if we add new features, we should fit scaler on them too.
            # So we should probably do a temporary transform to fit the scaler.
            X_transformed = self._transform_features(X)
            self.scaler.fit(X_transformed)
            
        return self
        
    def transform(self, X):
        # logger.info("🔄 Transforming features...")
        X_transformed = self._transform_features(X)
        
        if self.scaler:
            X_transformed = pd.DataFrame(
                self.scaler.transform(X_transformed),
                columns=X_transformed.columns,
                index=X_transformed.index
            )
            
        self.feature_names_out_ = X_transformed.columns.tolist()
        return X_transformed
        
    def _transform_features(self, X):
        X = X.copy()
        
        # Impute missing values
        if self.imputer:
            X[:] = self.imputer.transform(X)
            
        # Add interaction features
        if self.config.get('feature_engineering', {}).get('interaction_features', False):
            # Example interactions based on domain knowledge
            if 'Call  Failure' in X.columns and 'Subscription  Length' in X.columns:
                 X['Failure_Rate'] = X['Call  Failure'] / (X['Subscription  Length'] + 1)
            
            if 'Charge  Amount' in X.columns and 'Seconds of Use' in X.columns:
                X['Cost_Per_Second'] = X['Charge  Amount'] / (X['Seconds of Use'] + 1)
                
            if 'Frequency of use' in X.columns and 'Subscription  Length' in X.columns:
                X['Usage_Frequency_Per_Month'] = X['Frequency of use'] / (X['Subscription  Length'] + 1)

        # Add aggregation features (row-wise if applicable, or binning)
        if self.config.get('feature_engineering', {}).get('aggregation_features', False):
             # Total activity
             activity_cols = ['Frequency of use', 'Frequency of SMS', 'Distinct Called Numbers']
             existing_cols = [c for c in activity_cols if c in X.columns]
             if existing_cols:
                 X['Total_Activity'] = X[existing_cols].sum(axis=1)

        return X
