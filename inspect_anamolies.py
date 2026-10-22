
import pandas as pd

df = pd.read_csv("sensor_data_with_results.csv")

anomalies = df[df["ml_status"] == "Potential Anomaly"]

print("Total rows:", len(df))
print("Potential anomalies:", len(anomalies))

print("\nAnomaly readings:")
print(
    anomalies[
        ["time_ms", "temperature_C", "smoke_adc", "relay_on"]
    ].to_string(index=False)
)

print("\nMissing values:")
print(df[["temperature_C", "smoke_adc"]].isna().sum())

anomalies.to_csv("potential_anomalies.csv", index=False)
print("\nSaved: potential_anomalies.csv")
