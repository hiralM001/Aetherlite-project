import joblib
import pandas as pd

# Model load
model = joblib.load("space_weather_model.joblib")

# Input data (tame change kari sakso)
data = {
    'solar_wind_speed': [520],
    'bz': [-12],
    'proton_density': [18]
}
df = pd.DataFrame(data)

# Prediction
pred = model.predict(df)[0]
prob = model.predict_proba(df)[0][1] * 100

print("="*50)
print("AETHERGUARD - Space Weather Impact Report")
print("="*50)
print(f"Storm Prediction     : {'YES - Geomagnetic Storm' if pred == 1 else 'No Storm'}")
print(f"Storm Probability    : {prob:.2f}%")
print("-"*50)

# Cascading Impact Scoring
if pred == 1:
    if prob > 75:
        level = "SEVERE"
        satellite = "High risk - Satellite drag & communication blackout possible"
        power = "High risk - Power grid voltage fluctuations & transformer stress"
        aviation = "High risk - HF radio blackout & GPS degradation"
    elif prob > 50:
        level = "MODERATE"
        satellite = "Moderate risk - Minor orbital disturbances"
        power = "Moderate risk - Possible voltage irregularities"
        aviation = "Moderate risk - Occasional HF radio issues"
    else:
        level = "MILD"
        satellite = "Low risk"
        power = "Low risk"
        aviation = "Low risk"
else:
    level = "NONE"
    satellite = power = aviation = "Normal conditions"

print(f"Impact Level         : {level}")
print(f"Satellite Impact     : {satellite}")
print(f"Power Grid Impact    : {power}")
print(f"Aviation Impact      : {aviation}")
print("="*50)