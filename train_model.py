
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Load previously collected sensor data
df = pd.read_csv("sensor_data.csv")

features = ["temperature_C", "smoke_adc"]
X = df[features].copy()

# Create the ML pipeline
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("detector", IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    ))
])

# Train using collected sensor readings
model.fit(X)

# Save the complete trained pipeline
joblib.dump(model, "anomaly_model.joblib")

print("Model trained and saved successfully!")
print("Saved file: anomaly_model.joblib")
print("Features:", features)
