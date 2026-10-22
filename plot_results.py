
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sensor_data_with_results.csv")

# Convert elapsed milliseconds to elapsed minutes
df["elapsed_minutes"] = df["time_ms"] / 60000

normal = df["ml_status"] == "Normal"
anomaly = df["ml_status"] == "Potential Anomaly"

# Temperature graph
plt.figure(figsize=(12, 5))
plt.plot(
    df["elapsed_minutes"],
    df["temperature_C"],
    label="Temperature",
    linewidth=1
)
plt.scatter(
    df.loc[anomaly, "elapsed_minutes"],
    df.loc[anomaly, "temperature_C"],
    label="Potential anomaly",
    marker="x"
)
plt.xlabel("Elapsed time (minutes)")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Monitoring and ML Anomaly Detection")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("temperature_anomalies.png", dpi=150)
plt.show()

# MQ-2 graph
plt.figure(figsize=(12, 5))
plt.plot(
    df["elapsed_minutes"],
    df["smoke_adc"],
    label="MQ-2 raw ADC",
    linewidth=1
)
plt.scatter(
    df.loc[anomaly, "elapsed_minutes"],
    df.loc[anomaly, "smoke_adc"],
    label="Potential anomaly",
    marker="x"
)
plt.xlabel("Elapsed time (minutes)")
plt.ylabel("MQ-2 raw ADC value")
plt.title("MQ-2 Sensor Monitoring and ML Anomaly Detection")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("smoke_anomalies.png", dpi=150)
plt.show()

print("Saved temperature_anomalies.png")
print("Saved smoke_anomalies.png")
