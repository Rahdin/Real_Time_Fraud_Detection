from pydantic import BaseModel, Field
from datetime import datetime

class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: str
    amount: float = Field(..., gt=0, description="Transaction amount in CAD")
    merchant_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Feature needed for the ML model
    merchant_risk_score: float = Field(..., ge=0, le=100)

class FraudResult(BaseModel):
    is_fraud: bool
    risk_score: float
    reason: list[str]
    processed_at: datetime