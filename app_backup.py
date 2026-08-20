import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="AetherGuard", page_icon="🌌", layout="centered")

st.title("🌌 AetherGuard")
st.subheader("Multi-Modal AI Early-Warning System for Cascading Space-Weather Impacts")

# Model load
model = joblib.load("space_weather_model.joblib")

st.markdown("---")
st.write("### Enter Space Weather Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    solar_wind = st.number_input("Solar Wind Speed (km/s)", min_value=200, max_value=1000, value=450)

with col2:
    bz = st.number_input("Bz (nT)", min_value=-30, max_value=30, value=-5)

with col3:
    proton = st.number_input("Proton Density", min_value=1, max_value=50, value=8)

if st.button("Predict Impact", type="primary"):
    data = pd.DataFrame({
        'solar_wind_speed': [solar_wind],
        'bz': [bz],
        'proton_density': [proton]
    })

    pred = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1] * 100

    st.markdown("---")
    st.write("### Prediction Result")

    if pred == 1:
        st.error(f"⚠️ Geomagnetic Storm Detected — Probability: {prob:.1f}%")
    else:
        st.success(f"✅ No Storm — Probability of Storm: {prob:.1f}%")

    # Impact scoring
    if pred == 1:
        if prob > 75:
            level = "SEVERE"
            color = "red"
        elif prob > 50:
            level = "MODERATE"
            color = "orange"
        else:
            level = "MILD"
            color = "yellow"
    else:
        level = "NONE"
        color = "green"

    st.markdown(f"### Impact Level: :{color}[{level}]")

    st.write("**Satellite Impact:**", "High risk of drag & communication issues" if level in ["SEVERE", "MODERATE"] else "Normal")
    st.write("**Power Grid Impact:**", "Voltage fluctuations & transformer stress possible" if level in ["SEVERE", "MODERATE"] else "Normal")
    st.write("**Aviation Impact:**", "HF radio blackout & GPS degradation risk" if level in ["SEVERE", "MODERATE"] else "Normal")