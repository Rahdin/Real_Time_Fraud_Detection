import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib


def train_dummy_model():
    n_samples = 1000
    
    
    f1_amount = np.random.normal(50, 15, n_samples)
    
    
    f2_risk = np.random.randint(0, 20, n_samples)
    
   
    f3_hour = np.random.randint(0, 24, n_samples)
    
    
    X_normal = np.column_stack((f1_amount, f2_risk, f3_hour))
    
    
    n_anomalies = 50
    
    
    a1_amount = np.random.normal(2000, 500, n_anomalies)
    a2_risk = np.random.randint(50, 100, n_anomalies)
    a3_hour = np.random.randint(0, 24, n_anomalies)
    
    X_outliers = np.column_stack((a1_amount, a2_risk, a3_hour))
    
    
    X = np.vstack([X_normal, X_outliers])
    
    
    clf = IsolationForest(random_state=42, contamination=0.05)
    clf.fit(X)
    
    joblib.dump(clf, "app/isolation_forest.joblib")
   
if __name__ == "__main__":
    train_dummy_model()