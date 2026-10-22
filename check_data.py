
import pandas as pd

df = pd.read_csv("sensor_data.csv")

print("Dataset size:", df.shape)
print("\nFirst 5 readings:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSensor statistics:")
print(df[["temperature_C", "smoke_adc"]].describe())

print("\nRelay status counts:")
print(df["relay_on"].value_counts())
