from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np
from pymongo import MongoClient
import constants as const
from enums import Parameters, Components, probs

app = FastAPI()

# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Connect to MongoDB
client = MongoClient('mongodb+srv://303wspartan:GWQERLOFL7sTSmI7@cluster0.ahk9e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['recommendation_db']
collection = db['recommendations']

# Define the request model
class PredictionRequest(BaseModel):
    deviation: float = Field(..., description="Deviation value for the component")
    component: Components = Field(..., description="The component whose efficiency is being predicted")
    parameter: Parameters = Field(..., description="The parameter associated with the component")

# Function to fetch recommendations from the database
def get_recommendations(component_name, parameter_name):
    recommendations = collection.find_one({"component": component_name, "parameter": parameter_name})
    if recommendations:
        return recommendations.get("recommendations", ["No recommendations available."])
    else:
        return ["Recommendation not found."]

# Endpoint for predictions and recommendations
@app.post("/predict/")
def predict(request: PredictionRequest):
    # Normalize the input features
    deviation_min = const.deviation_min
    deviation_max = const.deviation_max
    prob_fail_min = const.prob_fail_min
    prob_fail_max = const.prob_fail_max

    deviation_normalized = (request.deviation - deviation_min) / (deviation_max - deviation_min)
    
    # Get the probability of failure based on the parameter
    if request.parameter.name not in probs:
        raise HTTPException(status_code=400, detail="Invalid parameter")
    
    probability_of_failure = probs[request.parameter.name]
    probability_of_failure_normalized = (probability_of_failure - prob_fail_min) / (prob_fail_max - prob_fail_min)

    # Prepare the input for the model
    X_input = np.array([[deviation_normalized, probability_of_failure_normalized]])

    # Make the prediction
    try:
        predicted_efficiency = model.predict(X_input)[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Model prediction error: {e}")

    # Determine if recommendations are needed
    if predicted_efficiency < 0.8:
        recommendations = get_recommendations(request.component.name, request.parameter.name)
    else:
        recommendations = ["SYSTEM OPTIMAL"]

    return {
        "deviation": request.deviation,
        "probability_of_failure": probability_of_failure,
        "predicted_efficiency": predicted_efficiency,
        "recommendations": recommendations
    }

@app.get('/')
def index():
    return {'message': 'This is the homepage of the API'}


@app.post('/update_recommendations/')   

@app.post('/update_recommendations/')
def update_recommendations():
    recommendations = [
        {
            "component": "ENGINE",
            "parameter": "ENGINE_OIL_PRESSURE",
            "recommendations": [
                "Check oil levels.",
                "Change the oil filter.",
                "Inspect the air filter for blockages."
            ],
            "efficiency_threshold": 80
        },
        {
            "component": "ENGINE",
            "parameter": "ENGINE_SPEED",
            "recommendations": [
                "Inspect the throttle body.",
                "Check for vacuum leaks.",
                "Ensure proper calibration of the throttle position sensor."
            ],
            "efficiency_threshold": 80
        },
        {
            "component": "ENGINE",
            "parameter": "ENGINE_TEMPERATURE",
            "recommendations": [
                "Check the coolant level.",
                "Inspect the radiator for blockages.",
                "Check the water pump for proper operation."
            ],
            "efficiency_threshold": 80
        },
        # Add more entries as needed
    ]

    # Insert data
    collection.insert_many(recommendations)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,debug=False)
