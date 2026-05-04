from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import joblib


model = joblib.load("models/fraud_model.pkl")
app = FastAPI()

# =========================
# LOAD MODEL (will load after training finishes)
# =========================
MODEL_PATH = "models/fraud_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except:
    model = None
    print("⚠️ Model not found yet. Waiting for training...")

# =========================
# INPUT SCHEMA
# =========================
class Transaction(BaseModel):
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float
    Hour: int
    Amount_log: float

# =========================
# HOME ROUTE
# =========================
@app.get("/")
def home():
    return {"message": "Fraud Detection API Running 🚀"}

# =========================
# PREDICTION ROUTE
# =========================
@app.post("/predict")
def predict(tx: Transaction):

    if model is None:
        return {"error": "Model not ready yet. Wait for training to finish."}

    try:
        # Convert input to DataFrame
        data = pd.DataFrame([tx.dict()])

        # Predict probability
        prob = model.predict_proba(data)[0][1]

        # Decision logic
        decision = "REVIEW" if prob > 0.3 else "ALLOW"

        return {
            "fraud_probability": round(prob, 4),
            "decision": decision
        }

    except Exception as e:
        return {"error": str(e)}
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/stats")
def stats():
    return {
        "total_transactions": 56962,
        "fraud_count": 492,
        "accuracy": 0.91
    }
    
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)