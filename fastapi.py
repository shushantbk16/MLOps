from fastapi import FastAPI 
import os
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()

@app.get("/")
def check():
    return "hello"

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)