from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np
from fastapi.security import HTTPBasic, HTTPBasicCredentials


#  FastAPI App

app = FastAPI(title="Intent Classification API", version="1.0")

security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "admin123"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return credentials.username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


#  Load Pre-trained Model & Artifacts

model = joblib.load("models/intent_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
le = joblib.load("models/label_encoder.pkl")


# Request / Response Schemas

class SingleQuery(BaseModel):
    text: str

class BatchQuery(BaseModel):
    texts: List[str]

class ClassificationResult(BaseModel):
    text: str
    intent: str
    confidence: float


# Endpoints


# Health check
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

# Model info (requires basic auth)
@app.get("/api/model/info")
def model_info(user: str = Depends(get_current_user)):
    info = {
        "model_name": "Trained Intent Classifier",
        "classes": list(le.classes_),
        "num_classes": len(le.classes_),
        # You can add real accuracy or metrics if you saved them
        "accuracy": 0.88
    }
    return info

# Classify single query
@app.post("/api/classify", response_model=ClassificationResult)
def classify_single(query: SingleQuery):
    if not query.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    X = vectorizer.transform([query.text])
    pred = model.predict(X)[0]
    conf = float(np.max(model.predict_proba(X)))
    intent = le.inverse_transform([pred])[0]
    return {"text": query.text, "intent": intent, "confidence": conf}

# Classify batch queries
@app.post("/api/classify/batch", response_model=List[ClassificationResult])
def classify_batch(batch: BatchQuery):
    if not batch.texts:
        raise HTTPException(status_code=400, detail="Text list cannot be empty")
    X = vectorizer.transform(batch.texts)
    preds = model.predict(X)
    probs = model.predict_proba(X)
    results = []
    for text, pred, prob in zip(batch.texts, preds, probs):
        intent = le.inverse_transform([pred])[0]
        conf = float(np.max(prob))
        results.append({"text": text, "intent": intent, "confidence": conf})
    return results
