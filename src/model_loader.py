import sys
import pickle
import joblib
import numpy as np
import logging
from .preprocessing import LogTransformer, clean_and_feature_engineer, select_features

# Configure logging
logger = logging.getLogger(__name__)

# Add our classes to the main module 
sys.modules['__main__'].LogTransformer = LogTransformer
sys.modules['__main__'].clean_and_feature_engineer = clean_and_feature_engineer
sys.modules['__main__'].select_features = select_features

def load_model(model_path):

    try:
        logger.info(f"Attempting to load model from {model_path}")
        model = joblib.load(model_path)
        
        # Debug  loaded model
        logger.info(f"Loaded model type: {type(model)}")
        if hasattr(model, 'steps'):
            logger.info("Pipeline steps:")
            for step_name, step in model.steps:
                logger.info(f"- {step_name}: {type(step)}")
        
        # Verify prediction methods
        if not (hasattr(model, 'predict') or hasattr(model, 'predict_proba')):
            raise ValueError(f"Loaded model doesn't have prediction methods. Got type: {type(model)}")
            
        return model
        
    except FileNotFoundError:
        logger.error(f"Model file not found: {model_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise RuntimeError(f"Failed to load model: {str(e)}") 