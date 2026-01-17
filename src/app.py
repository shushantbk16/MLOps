from fastapi import FastAPI 
from pydantic import BaseModel
import joblib


app = FastAPI()
model = joblib.load("models/sentiment_model.pkl")

class Request(BaseModel):
    text: str


@app.post("/predict")
def predict(req: Request):
    prediction = model.predict([req.text])[0]
    return {"sentiment": "Positive" if prediction == 1 else "Negative"}

@app.get("/")
def health():
    return {"status": "ok"}