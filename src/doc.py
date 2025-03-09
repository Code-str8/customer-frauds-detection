from fastapi import APIRouter, Response
from typing import List
from pydantic import BaseModel

router = APIRouter()

@router.get("/", summary="Welcome", tags=["Documentation"])
async def root():
    """
    Welcome to the Fraud Detection API!
    """
    return Response(
        content="Welcome to STEG Fraud Detection API! Visit /docs to see the documentation on how to use this API.",
        media_type="text/plain"
    )

@router.get("/docs", summary="API Documentation", tags=["Documentation"])
async def get_docs():
    """
    Documentation for the STEG Fraud Detection API.

    This API is designed to detect fraudulent activities in electricity and gas consumption based on billing data.
    
    The API expects the following features as input:

    - disrict: District code
    - client_catg: Client category
    - region: Region code
    - counter_type: Type of counter
    - consumption_level: Consumption level
    - counter_coefficient: Counter coefficient
    - invoice_year: Year of invoice
    - creation_year: Year of account creation
    - creation_month: Month of account creation

    To use the API, send a POST request to either:
    - '/stacked/predict' for the stacked model prediction
    - '/xgb/predict' for the XGBoost model prediction
    
    The API will return:
    - prediction: Whether the client is fraudulent (1) or not (0)
    - probability: The probability of fraud as a percentage
    """
    return