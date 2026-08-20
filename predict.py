import joblib
import pandas as pd

# Model load karo
model = joblib.load("space_weather_model.joblib")

# Example input (tame change kari sakso)
data = {
    'solar_wind_speed': [450],
    'bz': [-8],
    'proton_density': [12]
}

df = pd.DataFrame(data)

# Prediction
prediction = model.predict(df)
probability = model.predict_proba(df)

print("Storm Prediction:", "Yes (Storm)" if prediction[0] == 1 else "No Storm")
print("Storm Probability:", round(probability[0][1] * 100, 2), "%")