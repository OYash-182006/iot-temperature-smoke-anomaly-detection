
import serial
import pandas as pd
import joblib
import time

# Change COM6 if your Arduino uses a different port
PORT = "COM6"
BAUD_RATE = 9600

# Load the trained ML pipeline
model = joblib.load("anomaly_model.joblib")

print("Connecting to Arduino...")

try:
    arduino = serial.Serial(PORT, BAUD_RATE, timeout=2)
    time.sleep(2)  # Allow Arduino to reset

    print("Connected! Live anomaly detection started.")
    print("Press Ctrl+C to stop.\n")

    while True:
        line = arduino.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        if not line:
            continue

        # Skip CSV header or malformed lines
        parts = line.split(",")

        if len(parts) != 4:
            continue

        try:
            time_ms = int(parts[0])
            temperature = float(parts[1])
            smoke_adc = float(parts[2])
            relay_on = int(parts[3])

            # Use the same two features as during training
            sample = pd.DataFrame(
                [[temperature, smoke_adc]],
                columns=["temperature_C", "smoke_adc"]
            )

            prediction = model.predict(sample)[0]
            status = (
                "Normal" if prediction == 1
                else "Potential Anomaly"
            )

            print(
                f"Time: {time_ms} ms | "
                f"Temp: {temperature:.2f} C | "
                f"MQ-2 ADC: {smoke_adc:.0f} | "
                f"Relay: {relay_on} | "
                f"ML: {status}"
            )

        except (ValueError, IndexError):
            print("Skipped invalid sensor reading:", line)

except serial.SerialException as e:
    print("Serial connection error:", e)
    print("Close Arduino Serial Monitor and check the COM port.")

except KeyboardInterrupt:
    print("\nLive detection stopped.")

finally:
    if "arduino" in locals() and arduino.is_open:
        arduino.close()
