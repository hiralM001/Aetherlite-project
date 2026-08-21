import streamlit as st
import joblib
import pandas as pd
import requests
from datetime import datetime
import os
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="AetherGuard India", page_icon="🌌", layout="wide")

st.title("🌌 AetherGuard India")
st.markdown("**Low-Cost Cascading Impact Early Warning System for Space Weather**")
st.caption("Protecting NavIC • Power Grid • Indian Satellites | Live NOAA + History Graphs + Multi-User Alerts")

st.markdown("---")

# ====================== CONFIG ======================
SUBSCRIBERS_FILE = "subscribers.txt"
HISTORY_FILE = "prediction_history.csv"
USERS_FILE = "users.txt"

# Bot Token (hard-coded as requested)
BOT_TOKEN = "8753146565:AAH2qeuB4XzvcE-Btqy8hB0YzQbSFI-Pkac"

@st.cache_resource
def load_model():
    return joblib.load("space_weather_model.joblib")

model = load_model()

# ====================== SESSION STATE ======================
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False
if "solar" not in st.session_state:
    st.session_state.solar = 450.0
if "bz" not in st.session_state:
    st.session_state.bz = -5.0
if "proton" not in st.session_state:
    st.session_state.proton = 8.0
if "data_source" not in st.session_state:
    st.session_state.data_source = "Manual"
if "last_update" not in st.session_state:
    st.session_state.last_update = "-"
if "username" not in st.session_state:
    st.session_state.username = ""

# ====================== USER HELPERS ======================
def safe_username(name):
    safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_")).rstrip()
    return safe_name.replace(" ", "_")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_user(username):
    users = load_users()
    if username and username not in users:
        with open(USERS_FILE, "a") as f:
            f.write(username + "\n")

def get_history_filename():
    if st.session_state.username:
        return f"history_{safe_username(st.session_state.username)}.csv"
    return HISTORY_FILE

def load_history():
    filename = get_history_filename()
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_prediction(solar, bz, proton, storm_prob, level, navic_risk, grid_risk, sat_risk, source):
    if not st.session_state.username:
        st.warning("Please select or add a user first to save history.")
        return

    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "solar_wind": solar,
        "bz": bz,
        "proton": proton,
        "storm_prob": round(storm_prob, 2),
        "level": level,
        "navic_risk": navic_risk,
        "grid_risk": grid_risk,
        "sat_risk": sat_risk,
        "source": source,
        "username": st.session_state.username
    }

    df = load_history()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    if len(df) > 50:
        df = df.tail(50)
    df.to_csv(get_history_filename(), index=False)

def clear_current_user_history():
    if not st.session_state.username:
        return False, "Please select a user first."
    filename = get_history_filename()
    if os.path.exists(filename):
        try:
            os.remove(filename)
            return True, f"History cleared for {st.session_state.username}."
        except Exception as e:
            return False, f"Failed to clear history: {e}"
    return True, "No history found for current user."

# ====================== TELEGRAM HELPERS ======================
def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_subscriber(chat_id):
    subscribers = load_subscribers()
    if chat_id not in subscribers:
        with open(SUBSCRIBERS_FILE, "a") as f:
            f.write(chat_id + "\n")
        return True
    return False

def delete_subscriber(chat_id):
    subscribers = load_subscribers()
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        with open(SUBSCRIBERS_FILE, "w") as f:
            for sid in subscribers:
                f.write(sid + "\n")
        return True
    return False

def send_telegram_alert(message):
    if not BOT_TOKEN:
        return False, "BOT_TOKEN not configured."

    subscribers = load_subscribers()
    if not subscribers:
        return False, "No subscribers found."

    success_count = 0
    for chat_id in subscribers:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            res = requests.post(url, data=payload, timeout=10)
            if res.status_code == 200:
                success_count += 1
        except:
            pass

    return True, f"Alert sent to {success_count} subscribers."

def fetch_live_data():
    try:
        wind_url = "https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json"
        wind_data = requests.get(wind_url, timeout=10).json()
        mag_url = "https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json"
        mag_data = requests.get(mag_url, timeout=10).json()

        active_wind = next((item for item in wind_data if item.get("active") == True), None)
        active_mag = next((item for item in mag_data if item.get("active") == True), None)

        if active_wind and active_mag:
            speed = active_wind.get("proton_speed")
            density = active_wind.get("proton_density")
            bz_val = active_mag.get("bz_gsm")
            if speed is not None and density is not None and bz_val is not None:
                return {
                    "solar": round(float(speed), 1),
                    "proton": round(float(density), 2),
                    "bz": round(float(bz_val), 2),
                    "source": active_wind.get("source", "NOAA"),
                    "time": active_wind.get("time_tag", datetime.now().strftime("%Y-%m-%d %H:%M"))
                }
        return None
    except Exception as e:
        st.error(f"Live data fetch failed: {e}")
        return None

# ====================== USER DROPDOWN ======================
st.subheader("👤 User Identification")

users_list = load_users()
dropdown_options = [""] + users_list

selected_user = st.selectbox(
    "Select Username / Team Name",
    options=dropdown_options,
    index=dropdown_options.index(st.session_state.username) if st.session_state.username in dropdown_options else 0,
    key="selected_user_dropdown"
)

new_user = st.text_input("Or add new user", placeholder="Example: TeamAether")

col_user1, col_user2, col_user3 = st.columns([1, 1, 1])

with col_user1:
    if st.button("Set User"):
        final_user = selected_user.strip()
        if final_user:
            st.session_state.username = final_user
            save_user(final_user)
            st.success(f"Current user set to {final_user}")
            st.rerun()
        else:
            st.warning("Please select a username")

with col_user2:
    if st.button("Add New User"):
        final_user = new_user.strip()
        if final_user:
            st.session_state.username = final_user
            save_user(final_user)
            st.success(f"New user added: {final_user}")
            st.rerun()
        else:
            st.warning("Please enter a new username")

with col_user3:
    if st.button("Refresh Users"):
        st.rerun()

if st.session_state.username:
    st.info(f"Current user: **{st.session_state.username}**")
else:
    st.warning("No username selected yet")

st.markdown("---")

# ====================== QUICK ACTIONS ======================
st.subheader("🚀 Quick Actions")
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    if st.button("Quiet Scenario", use_container_width=True):
        st.session_state.solar = 380.0
        st.session_state.bz = 2.0
        st.session_state.proton = 5.0
        st.session_state.data_source = "Demo - Quiet"
        st.session_state.prediction_done = False
        st.rerun()

with col_b:
    if st.button("Moderate Storm", use_container_width=True):
        st.session_state.solar = 490.0
        st.session_state.bz = -9.0
        st.session_state.proton = 14.0
        st.session_state.data_source = "Demo - Moderate"
        st.session_state.prediction_done = False
        st.rerun()

with col_c:
    if st.button("Severe Storm", use_container_width=True):
        st.session_state.solar = 650.0
        st.session_state.bz = -16.0
        st.session_state.proton = 25.0
        st.session_state.data_source = "Demo - Severe"
        st.session_state.prediction_done = False
        st.rerun()

with col_d:
    if st.button("📡 Fetch Live NOAA Data", type="primary", use_container_width=True):
        live = fetch_live_data()
        if live:
            st.session_state.solar = live["solar"]
            st.session_state.bz = live["bz"]
            st.session_state.proton = live["proton"]
            st.session_state.data_source = f"Live NOAA ({live['source']})"
            st.session_state.last_update = live["time"]
            st.session_state.prediction_done = False
            st.success(f"Live data loaded! Source: {live['source']}")
            st.rerun()
        else:
            st.warning("Live data not available right now.")

st.markdown("---")

# ====================== INPUT SECTION ======================
st.subheader("📡 Space Weather Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    solar_wind = st.number_input("Solar Wind Speed (km/s)", min_value=200.0, max_value=1000.0, value=float(st.session_state.solar), step=1.0)
with col2:
    bz = st.number_input("Bz (nT)", min_value=-30.0, max_value=30.0, value=float(st.session_state.bz), step=0.1)
with col3:
    proton = st.number_input("Proton Density", min_value=0.1, max_value=50.0, value=float(st.session_state.proton), step=0.1)

st.session_state.solar = solar_wind
st.session_state.bz = bz
st.session_state.proton = proton

st.caption(f"Data Source: **{st.session_state.data_source}** | Last Update: {st.session_state.last_update}")
st.caption(
    f"Showing private history for: **{st.session_state.username}**"
    if st.session_state.username else
    "Set a Username above to start your private history."
)

if st.button("🔍 Predict Impact", type="primary", use_container_width=True):
    if not st.session_state.username:
        st.warning("Please set Username first.")
    else:
        data = pd.DataFrame({
            'solar_wind_speed': [solar_wind],
            'bz': [bz],
            'proton_density': [proton]
        })

        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0]
        storm_prob = proba[1] * 100

        if pred == 0:
            level = "Quiet"
            color = "green"
            emoji = "✅"
            navic_risk = grid_risk = sat_risk = "Low"
            navic_score = 20
            grid_score = 15
            sat_score = 18
            navic_msg = "NavIC accuracy normal"
            grid_msg = "Power grid stable"
            sat_msg = "Satellite operations normal"
            action = "No special action needed. Continue routine monitoring."
        elif storm_prob < 60:
            level = "Moderate"
            color = "orange"
            emoji = "⚠️"
            navic_risk = grid_risk = sat_risk = "Medium"
            navic_score = 55
            grid_score = 50
            sat_score = 60
            navic_msg = "Possible 2–5 meter accuracy degradation"
            grid_msg = "Minor voltage fluctuations possible in Northern Grid"
            sat_msg = "Increased surface charging risk on LEO satellites"
            action = "Increase monitoring frequency. Inform grid operators & satellite control."
        else:
            level = "Strong"
            color = "red"
            emoji = "🚨"
            navic_risk = grid_risk = sat_risk = "High"
            navic_score = 90
            grid_score = 85
            sat_score = 92
            navic_msg = "Significant accuracy loss possible (5–15 meters)"
            grid_msg = "High risk of voltage instability & transformer stress"
            sat_msg = "High risk of charging, drag increase & communication issues"
            action = "Activate safe-mode protocols. Alert ISRO / Power Grid operators immediately."

        save_prediction(solar_wind, bz, proton, storm_prob, level, navic_risk, grid_risk, sat_risk, st.session_state.data_source)

        st.session_state.prediction_done = True
        st.session_state.level = level
        st.session_state.storm_prob = storm_prob
        st.session_state.emoji = emoji
        st.session_state.color = color
        st.session_state.navic_risk = navic_risk
        st.session_state.grid_risk = grid_risk
        st.session_state.sat_risk = sat_risk
        st.session_state.navic_score = navic_score
        st.session_state.grid_score = grid_score
        st.session_state.sat_score = sat_score
        st.session_state.navic_msg = navic_msg
        st.session_state.grid_msg = grid_msg
        st.session_state.sat_msg = sat_msg
        st.session_state.action = action

        st.session_state.telegram_msg = f"""🌌 *AetherGuard India Alert*
Time: {datetime.now().strftime('%d-%m-%Y %H:%M')}

Storm Level: *{level}*
Probability: {storm_prob:.1f}%

🇮🇳 India Impact:
• NavIC: {navic_risk}
• Power Grid: {grid_risk}
• Satellites: {sat_risk}

Action: {action}
Data Source: {st.session_state.data_source}"""

# ====================== RESULTS ======================
if st.session_state.prediction_done:
    st.markdown("---")
    st.subheader("1. Next 12-Hour Prediction")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric("Storm Probability", f"{st.session_state.storm_prob:.1f}%")
        st.markdown(f"### {st.session_state.emoji} Storm Level: :{st.session_state.color}[{st.session_state.level}]")
    with col_b:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=st.session_state.storm_prob,
            title={'text': "Storm Probability %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkred" if st.session_state.storm_prob > 70 else "orange" if st.session_state.storm_prob > 40 else "green"},
                'steps': [
                    {'range': [0, 40], 'color': "#1a3a1a"},
                    {'range': [40, 70], 'color': "#3a3a1a"},
                    {'range': [70, 100], 'color': "#3a1a1a"}
                ],
            }
        ))
        fig_gauge.update_layout(height=250, template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    st.subheader("2. India-Specific Cascading Impact")

    impact_df = pd.DataFrame({
        "System": ["NavIC", "Power Grid", "Satellites"],
        "Risk Score": [st.session_state.navic_score, st.session_state.grid_score, st.session_state.sat_score],
        "Level": [st.session_state.navic_risk, st.session_state.grid_risk, st.session_state.sat_risk]
    })

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        fig_impact = px.bar(
            impact_df, x="System", y="Risk Score", color="Level",
            color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"},
            text="Risk Score", title="Cascading Impact Risk Scores"
        )
        fig_impact.update_layout(height=280, template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_impact, use_container_width=True)

    with col_right:
        st.info(f"**🛰️ NavIC**\n\n**{st.session_state.navic_risk} Risk**\n\n{st.session_state.navic_msg}")
        st.info(f"**⚡ Power Grid**\n\n**{st.session_state.grid_risk} Risk**\n\n{st.session_state.grid_msg}")
        st.info(f"**📡 Satellites**\n\n**{st.session_state.sat_risk} Risk**\n\n{st.session_state.sat_msg}")

    st.markdown("---")
    st.subheader("3. Recommended Action")
    st.success(st.session_state.action)

# ====================== HISTORY GRAPHS ======================
st.markdown("---")
st.subheader("📈 Prediction History Graphs")

st.markdown("##### History Actions")
col_h1, col_h2 = st.columns([1, 1])

with col_h1:
    if st.button("🗑️ Clear My History", type="secondary", use_container_width=True):
        success, msg = clear_current_user_history()
        if success:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

with col_h2:
    if st.session_state.username:
        st.info(f"Current user: {st.session_state.username}")
    else:
        st.warning("Set a Username first")

history_df = load_history()

if not history_df.empty:
    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
    history_df = history_df.sort_values("timestamp")

    fig_prob = px.line(
        history_df,
        x="timestamp",
        y="storm_prob",
        title="Storm Probability Over Time",
        markers=True,
        color_discrete_sequence=["#ff6b6b"]
    )
    fig_prob.update_layout(height=320, template="plotly_dark", yaxis_title="Probability %")
    st.plotly_chart(fig_prob, use_container_width=True)

    fig_params = go.Figure()
    fig_params.add_trace(go.Scatter(x=history_df["timestamp"], y=history_df["solar_wind"], name="Solar Wind", line=dict(color="#00d4ff")))
    fig_params.add_trace(go.Scatter(x=history_df["timestamp"], y=history_df["bz"], name="Bz", line=dict(color="#ff6b6b")))
    fig_params.add_trace(go.Scatter(x=history_df["timestamp"], y=history_df["proton"], name="Proton Density", line=dict(color="#ffe66d")))
    fig_params.update_layout(title="Space Weather Parameters History", height=320, template="plotly_dark")
    st.plotly_chart(fig_params, use_container_width=True)

    st.write("**Recent Predictions:**")
    st.dataframe(history_df.tail(10).sort_values("timestamp", ascending=False), use_container_width=True)
else:
    st.info("No prediction history yet. Click **Predict Impact** to start storing history.")

# ====================== TELEGRAM SECTION ======================
st.markdown("---")
st.subheader("4. Telegram Alert System")

if st.session_state.prediction_done:
    st.code(st.session_state.telegram_msg)

subscribers = load_subscribers()
st.write(f"**Total Subscribers:** {len(subscribers)}")

st.markdown("##### Add New Subscriber")
new_chat_id = st.text_input("Enter Chat ID to add", placeholder="Example: 123456789")
if st.button("➕ Add Subscriber"):
    if new_chat_id.strip():
        added = save_subscriber(new_chat_id.strip())
        if added:
            st.success("Chat ID added successfully!")
            st.rerun()
        else:
            st.info("This Chat ID is already registered.")
    else:
        st.warning("Please enter a valid Chat ID")

st.markdown("##### Remove Subscriber")
remove_chat_id = st.text_input("Enter Chat ID to remove", placeholder="Enter ID to delete")
if st.button("🗑️ Remove Subscriber"):
    if remove_chat_id.strip():
        deleted = delete_subscriber(remove_chat_id.strip())
        if deleted:
            st.success("Chat ID removed successfully!")
            st.rerun()
        else:
            st.warning("This Chat ID was not found.")
    else:
        st.warning("Please enter a Chat ID")

if st.session_state.prediction_done:
    if st.button("📤 Send Alert to All Subscribers", type="primary"):
        success, msg = send_telegram_alert(st.session_state.telegram_msg)
        if success:
            st.success(msg)
            st.balloons()
        else:
            st.error(msg)