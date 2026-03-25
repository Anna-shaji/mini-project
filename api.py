from fastapi import FastAPI
import pandas as pd
import joblib
import shap
import numpy as np

app = FastAPI()

# 1. Load Model and Column structure
model = joblib.load("models/churn_model.pkl")
columns = joblib.load("models/columns.pkl")

# 2. Initialize SHAP Explainer
explainer = shap.TreeExplainer(model)

@app.post("/predict")
def predict(data: dict):
    # --- PREPROCESSING ---
    # Convert incoming JSON to DataFrame
    # We wrap 'data' in another list to ensure it's treated as one row
    df = pd.DataFrame([data])
    
    # Handle Categorical Encoding
    df = pd.get_dummies(df)
    
    # Ensure columns match training features
    # 'columns' is already a list, so we don't need .tolist() later
    df = df.reindex(columns=columns, fill_value=0)

    # --- MODEL PREDICTION ---
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    # --- SHAP EXPLANATION ---
    shap_values = explainer.shap_values(df)
    
    # Handle SHAP output logic
    if isinstance(shap_values, list):
        # Index 1 is usually the "Churn" class
        current_shap = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
    else:
        current_shap = shap_values[0]

    # --- RISK LOGIC ---
    if probability < 0.3:
        risk = "Low"
    elif probability < 0.7:
        risk = "Medium"
    else:
        risk = "High"

    # --- FINAL RESPONSE ---
    return {
        "prediction": int(prediction),
        "probability": round(float(probability), 4),
        "risk": risk,
        "shap_values": current_shap.tolist(), # current_shap is a numpy array, so .tolist() is correct here
        "feature_names": list(columns) # FIXED: Use list() constructor instead of .tolist()
    }