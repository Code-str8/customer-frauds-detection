from fastapi import FastAPI
from src.preprocessing import LogTransformer
from src.model_loader import load_model
from src.stacked import router as stacked_router
from src.xgb import router as xgb_router
from src.doc import router as doc_router

app = FastAPI(
    title="Fraud Detection API",
    description="API for detecting fraudulent electricity and gas consumption",
    version="1.0.0"
)

# Include the routers
app.include_router(doc_router)
app.include_router(stacked_router)
app.include_router(xgb_router)