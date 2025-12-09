import joblib
import redis
import os
import numpy as np
from datetime import datetime

class FraudDetector:
    def __init__(self):
        # Load the ML Model
        try:
            self.model = joblib.load("app/isolation_forest.joblib")
        except FileNotFoundError:
            self.model = None # Handle gracefully if model isn't trained yet

        # Connect to Redis (Cache)
        redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

    def check_velocity(self, user_id: str) -> bool:
        """
        Rule: Flag if user makes > 3 transactions in 60 seconds.
        """
        key = f"tx_count:{user_id}"
        
        # Atomically increment transaction count
        current_count = self.redis.incr(key)
        
        # If it's the first transaction, set expiry for 60 seconds
        if current_count == 1:
            self.redis.expire(key, 60)
            
        return current_count > 3
    

def predict_anomaly(self, amount: float, risk_score: float) -> bool:
        """
        Uses Isolation Forest to detect mathematical outliers.
        """
        if not self.model:
            return False
            
        # Format input for scikit-learn [amount, risk_score, current_hour]
        hour = datetime.now().hour
        features = np.array([[amount, risk_score, hour]])
        
        # Prediction: 1 is Normal, -1 is Anomaly
        prediction = self.model.predict(features)
        return prediction[0] == -1
