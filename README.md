# AetherGuard-INDIA
# 🌌 AetherGuard-INDIA

**AI-Powered Space Weather Prediction & Impact Assessment System**
*Forecasting solar flares and geomagnetic storms to protect India's critical infrastructure*

[🚀 Live Demo](#-quick-start) • [📖 Documentation](#-usage-guide) • [🔧 Installation](#-quick-start) • [🤝 Contributing](#-contributing)

---

## 🌟 Overview

**AetherGuard-INDIA** is a machine learning-powered platform that predicts space weather events — solar flares and geomagnetic storms — and assesses their potential impact on satellites, power grids, communication networks, and other infrastructure. The system combines historical space weather data with a trained prediction model to deliver early warnings through a simple, accessible web interface.

### 🎯 Mission

Give India's infrastructure operators, researchers, and the public an early-warning system for space weather disruptions, so that satellite operators, grid operators, and aviation/communication services can prepare before an event hits.

---

## ✨ Key Features

### 🤖 **Predictive Modeling**
- Machine learning model trained on historical space weather data (`space_weather_model.joblib`)
- Forecasts the likelihood and severity of solar flare / geomagnetic storm activity
- Continuously retrainable pipeline via `train_model.py`

### 📊 **Impact Assessment**
- Translates raw predictions into practical impact categories (`impact.py`) — e.g. effects on satellites, power grids, GPS, and radio communications
- Helps non-technical users understand *what a prediction means* rather than just a raw probability

### 🌐 **Web Dashboard**
- Lightweight Flask web app (`app.py`) for running predictions and viewing results
- Simple interface designed for quick checks without needing to run scripts manually

### 📁 **Historical Tracking**
- Prediction history logged per session/user (`history_Space.csv`, `history_default_username.csv`, `prediction_history.csv`)
- Enables trend review and comparison of past forecasts against outcomes

### 👥 **User & Subscriber Management**
- Basic user accounts (`users.txt`) for tracking who ran which predictions
- Subscriber list (`subscribers.txt`) to support alert/notification distribution

---

## 🏗️ System Architecture

### **Prediction Pipeline**

```
Space Weather Data → Feature Preparation → Trained ML Model (predict.py) →
Risk/Impact Scoring (impact.py) → Web Dashboard (app.py) → History Log
```

### **Core Components**

- **🧠 Prediction Engine**: `predict.py` — loads `space_weather_model.joblib` and generates forecasts
- **📉 Impact Engine**: `impact.py` — converts predictions into infrastructure impact assessments
- **🏋️ Training Pipeline**: `train_model.py` — trains/retrains the space weather model
- **🌐 Web Interface**: `app.py` — Flask-based dashboard for interacting with the system
- **💾 Data Store**: CSV-based history logs for predictions and user activity

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **pip** package manager
- **Git** for version control

### 1️⃣ Clone Repository

```bash
git clone https://github.com/hiralM001/Aetherlite-project.git
cd Aetherlite-project
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Launch Application

```bash
python app.py
```

### 4️⃣ Access Dashboard

Open your browser and navigate to:

- **Main Dashboard**: https://aetherlite-project-ehaceuxwfwyfhbdd7txgqh.streamlit.app/

---

## 📋 Usage Guide

### **Web Interface**

1. **Open the dashboard** in your browser after starting `app.py`
2. **Run a prediction** using the current/latest space weather inputs
3. **Review results**, including the predicted event likelihood and impact assessment
4. **Check history** to compare against past predictions

### **Command Line**

```bash
# Run a prediction directly
python predict.py

# Assess impact of a given prediction
python impact.py

# Retrain the model on updated data
python train_model.py
```

---

## 📁 Project Structure

```
Aetherlite-project/
├── 📂 .devcontainer/              # Dev container configuration
├── 🌐 app.py                      # Flask web application (main entry point)
├── 🗄️ app_backup.py               # Backup copy of the web application
├── 🧠 predict.py                  # Prediction script using the trained model
├── 📉 impact.py                   # Converts predictions into impact assessments
├── 🏋️ train_model.py              # Model training / retraining script
├── 🤖 space_weather_model.joblib  # Trained ML model artifact
├── 📊 history_Space.csv           # Space weather prediction history
├── 📊 history_default_username.csv# Per-user prediction history
├── 📊 prediction_history.csv      # General prediction log
├── 👤 users.txt                   # Registered users
├── 📧 subscribers.txt             # Alert subscriber list
├── 📋 requirements.txt            # Python dependencies
└── 📖 README.md                   # This file
```

---

## 🎯 Use Cases

### **Satellite Operators**
- Anticipate solar activity that may affect satellite electronics or communications

### **Power Grid Operators**
- Early warning for geomagnetically induced currents that can stress transformers

### **Researchers & Students**
- Study space weather trends using logged historical prediction data
- Experiment with retraining the model on new data

### **General Public / Enthusiasts**
- Check current space weather risk through a simple web dashboard

---

## 🛠️ Development

### **Setting Up a Development Environment**

```bash
# Clone repository
git clone https://github.com/hiralM001/Aetherlite-project.git
cd Aetherlite-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### **Retraining the Model**

```bash
python train_model.py
```

This regenerates `space_weather_model.joblib` using the latest training data.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

### **Contribution Areas**
- 🧠 **Model Improvements**: Improve prediction accuracy or add new features
- 📉 **Impact Logic**: Refine how predictions map to real-world impact categories
- 🎨 **UI/UX**: Improve the Flask dashboard
- 📚 **Documentation**: Help others understand and use the system

### **Development Workflow**

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Submit** a Pull Request with a detailed description

---

## 📜 License

No license has been specified for this project yet. Consider adding one (e.g. MIT) so others know how they can use and contribute to it.

---

## 📞 Support & Contact

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/hiralM001/Aetherlite-project/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/hiralM001/Aetherlite-project/discussions)

---

**🌌 Forecasting the Skies to Protect What's on the Ground**
