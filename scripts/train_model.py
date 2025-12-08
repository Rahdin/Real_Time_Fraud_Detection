import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import logging

# Configure logging (Industry Best Practice)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_dummy_model():
    logger.info("Generating synthetic banking data...")
    
    # Simulate 1000 normal transactions
    # Features: [amount, merchant_risk_score, time_of_day_hour]
    # Normal: Amounts ~$50, low risk score
    X_normal = 50 + 10 * np.random.randn(1000, 3) 
    
    # Simulate 50 fraudulent transactions (Anomalies)
    # Fraud: Amounts ~$5000, high risk score
    X_outliers = 5000 + 1000 * np.random.randn(50, 3)
    
    X = np.vstack([X_normal, X_outliers])
    
    # Train Isolation Forest (Unsupervised Anomaly Detection)
    # contamination=0.05 means we expect ~5% of data to be fraud
    clf = IsolationForest(random_state=42, contamination=0.05)
    clf.fit(X)
    
    # Save the model to be loaded by the API later
    model_path = "app/isolation_forest.joblib"
    joblib.dump(clf, model_path)
    logger.info(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_dummy_model(