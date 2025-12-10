"""
This file contains the FraudDetector class which implements
the core fraud detection logic which includes transcation velocity checks and
feeding the pre-trained ML model the transaction features for anomaly detection.

"""

import joblib
import redis
import os
import numpy as np
from datetime import datetime

class FraudDetector:
    def __init__(self):
        
        try:
            self.model = joblib.load("app/isolation_forest.joblib")
        except FileNotFoundError:
            print("WARNING: Model file not found. ML features will be disabled.")
            self.model = None 

        
        redis_url = os.getenv("REDIS_URL") 
        
        try:
            if redis_url:
               
                self.redis = redis.from_url(redis_url, decode_responses=True, ssl_cert_reqs=None)
            else:
                
                self.redis = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
                
            
            self.redis.ping()
            
        except redis.exceptions.ConnectionError:
            print("WARNING: Redis connection failed. Velocity checks disabled.")
           

    def check_velocity(self, user_id: str) -> bool:
       
        key = f"tx_count:{user_id}"
        
        
        current_count = self.redis.incr(key)
        
       
        if current_count == 1:
            self.redis.expire(key, 60)
            
        return current_count > 3
    

    def predict_anomaly(self, amount: float, risk_score: float) -> bool:
    
            if not self.model:
                return False
            
       
            hour = datetime.now().hour
            features = np.array([[amount, risk_score, hour]])
        
    
            prediction = self.model.predict(features)
            return prediction[0] == -1
