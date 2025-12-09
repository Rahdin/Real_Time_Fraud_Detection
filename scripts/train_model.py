"""
This file containts the script to train a dummy Isolation Forest model
on synthetic banking transaction data for fraud detection.

"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_dummy_model():
    logger.info("Generating synthetic banking data...")
    
  
    X_normal = 50 + 10 * np.random.randn(1000, 3) 
    
   
    X_outliers = 5000 + 1000 * np.random.randn(50, 3)
    
    X = np.vstack([X_normal, X_outliers])
    
    
    clf = IsolationForest(random_state=42, contamination=0.05)
    clf.fit(X)
    
   
    model_path = "app/isolation_forest.joblib"
    joblib.dump(clf, model_path)
    logger.info(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_dummy_model()