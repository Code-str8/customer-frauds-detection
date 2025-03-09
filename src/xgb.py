from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import logging
import traceback
from .preprocessing import LogTransformer
from .model_loader import load_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    logger.info("Attempting to load XGB model...")
    xgb_model = load_model('models/xgb_pipeline.joblib')
    logger.info("Successfully loaded XGB model")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    logger.error(traceback.format_exc())
    xgb_model = None

class FraudInput(BaseModel):
    counter_number: int
    account_age_days: int
    new_index: int
    old_index: int
    consumption_level_1: float
    counter_coefficient: float
    client_catg: int
    invoice_year: int
    creation_year: int
    creation_month: int

# Router 
router = APIRouter(
    prefix="/xgb",
    tags=["XGBoost Model"]
)

@router.post("/predict")
async def predict_fraud(data: FraudInput):
    if xgb_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    try:
        logger.info("Converting input to DataFrame")
        # input to DataFrame
        df = pd.DataFrame([data.dict()])
        logger.info(f"Input data: {df.to_dict()}")
        
        logger.info("Making prediction")
        # prediction and probability
        try:
            pred_proba = xgb_model.predict_proba(df)
            pred = xgb_model.predict(df)
            prob = pred_proba[0][1] * 100  
        except AttributeError:
            # If predict_proba not available, just use predict
            pred = xgb_model.predict(df)
            prob = 100 if pred[0] == 1 else 0
        
        result = {
            "prediction": int(pred[0]),
            "probability": f"{prob:.1f}%",
            "prediction_text": "Fraudulent" if pred[0] == 1 else "Non-Fraudulent"
        }
        logger.info(f"Prediction result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))