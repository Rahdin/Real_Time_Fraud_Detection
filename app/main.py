from fastapi import FastAPI, HTTPException, Depends
from app.schemas import TransactionRequest, FraudResult
from app.detector import FraudDetector
from datetime import datetime
import logging

# Initialize App and Logging
app = FastAPI(title="Fraud Detection")
logger = logging.getLogger("uvicorn")

# Dependency Injection for the Detector
# (Prevents reloading the model on every request)
detector = FraudDetector()

def get_detector():
    return detector

@app.post("/analyze", response_model=FraudResult)
async def analyze_transaction(
    tx: TransactionRequest, 
    engine: FraudDetector = Depends(get_detector)
):
    logger.info(f"Analyzing transaction {tx.transaction_id} for user {tx.user_id}")
    
    reasons = []
    is_fraud = False
    
    # Check 1: Velocity Rule (Redis)
    if engine.check_velocity(tx.user_id):
        is_fraud = True
        reasons.append("HIGH_VELOCITY_TRIGGER")
        
    # Check 2: ML Model (Isolation Forest)
    if engine.predict_anomaly(tx.amount, tx.merchant_risk_score):
        is_fraud = True
        reasons.append("ML_ANOMALY_DETECTED")
        
    return {
        "is_fraud": is_fraud,
        "risk_score": 0.95 if is_fraud else 0.05,
        "reason": reasons,
        "processed_at": datetime.now()
    }

@app.get("/health")
def health_check():
    return {"status": "active", "model_loaded": detector.model is not None}