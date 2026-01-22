import joblib
import pandas as pd

try:
    feature_names = joblib.load('backend/feature_names.pkl')
    print("Feature Names:", feature_names)
    
    metadata = joblib.load('backend/model_metadata.pkl')
    print("Metadata:", metadata)
except Exception as e:
    print(e)
