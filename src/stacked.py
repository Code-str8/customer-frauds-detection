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

# model path 
MODEL_PATH = 'models/stacked_pipeline.joblib'


try:
    logger.info("Attempting to load stacked model...")
    stacked_model = load_model(MODEL_PATH)
    logger.info("Successfully loaded stacked model")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    logger.error(traceback.format_exc())
    stacked_model = None

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
    prefix="/stacked",
    tags=["Stacked Model"]
)

@router.post("/predict")
async def predict_fraud(input_data: FraudInput):
    """
    Predict fraud using the stacked model
    """
    if stacked_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    try:
        logger.info("Converting input to DataFrame")
        # input to DataFrame
        df = pd.DataFrame([input_data.dict()])
        logger.info(f"Input data: {df.to_dict()}")
        
        logger.info("Making prediction")
        #prediction and probability
        try:
            pred_proba = stacked_model.predict_proba(df)
            pred = stacked_model.predict(df)
            prob = pred_proba[0][1] * 100  
        except AttributeError as e:
            logger.warning(f"predict_proba not available: {str(e)}")
            # If predict_proba not available, just use predict
            pred = stacked_model.predict(df)
            prob = 100 if pred[0] == 1 else 0
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error making prediction: {str(e)}"
            )
        
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
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )