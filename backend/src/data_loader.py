import pandas as pd
from ucimlrepo import fetch_ucirepo
import logging

logger = logging.getLogger(__name__)

def load_data(uci_id: int):
    """
    Fetches the dataset from UCI repository.
    """
    logger.info(f"🚀 Fetching UCI dataset ID {uci_id}...")
    try:
        dataset = fetch_ucirepo(id=uci_id)
        X = dataset.data.features
        y = dataset.data.targets
        
        # Flatten y if it's a dataframe
        if isinstance(y, pd.DataFrame):
            y = y.iloc[:, 0]
            
        logger.info(f"✅ Dataset loaded: {X.shape[0]} rows, {X.shape[1]} features")
        return X, y
    except Exception as e:
        logger.error(f"❌ Error fetching dataset: {e}")
        raise e
