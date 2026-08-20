import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

print("Model training shuru thay che...")

# Sample data (hackathon mate sufficient che)
np.random.seed(42)
data = {
    'solar_wind_speed': np.random.uniform(300, 700, 500),
    'bz': np.random.uniform(-20, 10, 500),
    'proton_density': np.random.uniform(1, 20, 500),
    'storm': np.random.randint(0, 2, 500)
}

df = pd.DataFrame(data)

X = df[['solar_wind_speed', 'bz', 'proton_density']]
y = df['storm']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(n_estimators=50, max_depth=3)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

joblib.dump(model, 'space_weather_model.joblib')
print("Model successfully save thai gayu --> space_weather_model.joblib")