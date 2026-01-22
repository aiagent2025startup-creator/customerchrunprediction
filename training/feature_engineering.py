import pandas as pd
import numpy as np

def create_interaction_features(df):
    """
    Create interaction features to capture non-linear relationships.
    """
    df = df.copy()
    
    # Interaction: Usage Intensity = Seconds of Use / Subscription Length
    # Avoid division by zero
    df['Usage_Per_Month'] = df['Seconds of Use'] / (df['Subscription  Length'] + 1e-5)
    
    # Interaction: Complaints per Month
    df['Complains_Per_Month'] = df['Complains'] / (df['Subscription  Length'] + 1e-5)
    
    # Interaction: Value per Use
    df['Value_Per_Second'] = df['Customer Value'] / (df['Seconds of Use'] + 1e-5)
    
    return df

def log_transform_skewed(df, columns):
    """
    Apply log transformation to skewed numerical features.
    """
    df = df.copy()
    for col in columns:
        if col in df.columns:
            # log1p handles zeros gracefully
            df[f'Log_{col}'] = np.log1p(df[col])
    return df

def bin_features(df):
    """
    Bin continuous features into categories.
    """
    df = df.copy()
    
    # Bin Age into groups if not already present or to refine
    if 'Age' in df.columns:
        df['Age_Bin'] = pd.cut(df['Age'], bins=[0, 18, 30, 45, 60, 100], labels=[0, 1, 2, 3, 4])
        
    return df

def preprocess_data(df):
    """
    Master pipeline for feature engineering.
    """
    # 1. Interactions
    df = create_interaction_features(df)
    
    # 2. Log Transform
    skewed_cols = ['Seconds of Use', 'Frequency of use', 'Frequency of SMS']
    df = log_transform_skewed(df, skewed_cols)
    
    # 3. Binning
    df = bin_features(df)
    
    return df
