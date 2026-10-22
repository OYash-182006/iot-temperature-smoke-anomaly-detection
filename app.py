
import time
import joblib
import serial
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ---------- PAGE SETUP ----------
st.set_page_config(
    page_title="IoT ML Monitoring",
    page_icon="🌡️",
    layout="wide"
)

st.title("IoT Temperature & Smoke Monitoring")
st.caption(
    "Arduino Uno + DS18B20 + MQ-2 + "
    "Machine Learning Anomaly Detection"
)

MODEL_PATH = "anomaly_model.joblib"
PORT = "COM6"
BAUD_RATE = 9600

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load ML model: {e}")
    st.stop()

# ---------- SESSION STATE ----------
if "ser" not in st.session_state:
    st.session_state.ser = None

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- SIDEBAR ----------
st.sidebar.header("Connection Settings")
st.sidebar.write(f"Serial port: {PORT}")
st.sidebar.write(f"Baud rate: {BAUD_RATE}")

col1, col2 = st.sidebar.columns(2)

if col1.button("Connect", use_container_width=True):
    try:
        if st.session_state.ser is not None:
            if st.session_state.ser.is_open:
                st.session_state.ser.close()

        st.session_state.ser = serial.Serial(
            PORT, BAUD_RATE, timeout=0.2
        )
        time.sleep(2)
        st.sidebar.success("Connected to Arduino")
    except Exception as e:
        st.session_state.ser = None
        st.sidebar.error(f"Connection failed: {e}")

if col2.button("Disconnect", use_container_width=True):
    if st.session_state.ser is not None:
        try:
            st.session_state.ser.close()
        except Exception:
            pass
        st.session_state.ser = None

ser = st.session_state.ser
connected = ser is not None and ser.is_open

if connected:
    st.sidebar.success("Arduino connected")
    st_autorefresh(interval=1000, key="refresh")
else:
    st.sidebar.warning("Arduino disconnected")
    st.info("Connect the Arduino using the sidebar to begin.")

# ---------- READ SENSOR DATA ----------
if connected:
    try:
        # Process any complete lines waiting in the serial buffer.
        while ser.in_waiting:
            line = ser.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            if not line:
                continue

            parts = line.split(",")

            # Expected format:
            # time_ms,temperature_C,smoke_adc,relay_on
            if len(parts) != 4:
                continue

            try:
                time_ms = float(parts[0])
                temperature = float(parts[1])
                smoke_adc = float(parts[2])
                relay_on = int(float(parts[3]))
            except ValueError:
                # Skips CSV header lines or invalid readings.
                continue

            sample = pd.DataFrame(
                [[temperature, smoke_adc]],
                columns=["temperature_C", "smoke_adc"]
            )

            prediction = int(model.predict(sample)[0])
            score = float(model.decision_function(sample)[0])

            status = (
                "Potential Anomaly"
                if prediction == -1
                else "Normal"
            )

            st.session_state.history.append({
                "Time (ms)": time_ms,
                "Temperature (°C)": temperature,
                "MQ-2 ADC": smoke_adc,
                "Relay": "ON" if relay_on == 1 else "OFF",
                "ML Status": status,
                "Decision Score": score
            })

            # Keep the most recent 500 readings.
            st.session_state.history = (
                st.session_state.history[-500:]
            )

    except (serial.SerialException, OSError) as e:
        st.error(f"Serial reading error: {e}")

# ---------- DASHBOARD ----------
df = pd.DataFrame(st.session_state.history)

if not df.empty:
    latest = df.iloc[-1]

    st.subheader("Live Sensor Readings")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Temperature",
        f"{latest['Temperature (°C)']:.2f} °C"
    )
    m2.metric(
        "MQ-2 Raw Reading",
        f"{latest['MQ-2 ADC']:.0f}"
    )
    m3.metric("Arduino Relay", latest["Relay"])
    m4.metric("ML Prediction", latest["ML Status"])

    st.divider()
    st.subheader("Sensor Graphs")

    left, right = st.columns(2)

    with left:
        st.write("Temperature over recent readings")
        st.line_chart(
            df.set_index("Time (ms)")["Temperature (°C)"]
        )

    with right:
        st.write("MQ-2 sensor readings over recent readings")
        st.line_chart(
            df.set_index("Time (ms)")["MQ-2 ADC"]
        )

    st.divider()
    st.subheader("Anomaly Summary")

    anomalies = df[df["ML Status"] == "Potential Anomaly"]

    a1, a2 = st.columns(2)
    a1.metric("Readings Received", len(df))
    a2.metric("Potential Anomalies", len(anomalies))

    st.caption(
        "An anomaly is an unusual sensor pattern, not proof "
        "of a fire or confirmed smoke event."
    )

    st.subheader("Recent Readings")
    st.dataframe(df.tail(20), use_container_width=True)

    st.download_button(
        "Download Dashboard Data as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="dashboard_sensor_data.csv",
        mime="text/csv"
    )

else:
    st.info("Waiting for valid sensor readings from Arduino.")

st.caption(
    "The ML model runs on the computer. The Arduino relay "
    "continues to follow its existing threshold-based logic."
)
