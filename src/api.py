import os
import mlflow
import dotenv
import uvicorn
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# Load environment variables
dotenv.load_dotenv("../.env")

# Set up mlflow tracking server and model
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
CHOSEN_MODEL = os.getenv("MODEL_ALIAS")

# Set mlflow url location
mlflow.set_tracking_uri(uri = MLFLOW_TRACKING_URI)

# Set mlflow experiment name
mlflow.set_experiment("Flower Classification")

# Set up pyfunc to load model
model = mlflow.pyfunc.load_model(f"models:/Untouch Logistic Regression@{CHOSEN_MODEL}")

# Set up predictor
class api_data(BaseModel):
    x1 : float
    x2 : float
    x3 : float
    x4 : float
    
# Create FastAPI Object
app = FastAPI()

# Create home object
@app.get("/")
def home():
    return "Hello, FastAPI UP!"

# Create predict object
@app.post("/predict/")
def predict(data: api_data):
    data = np.array([[data.x1, data.x2, data.x3, data.x4]]).astype(np.float64)
    y_pred = int(model.predict(data)[0])
    
    return {"res" : y_pred, "error_msg": ""}

if __name__ == "__main__":
    uvicorn.run("api:app", host = "0.0.0.0", port = 8080)