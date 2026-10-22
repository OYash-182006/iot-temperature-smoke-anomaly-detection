
import csv
import serial
import time

PORT = "COM6"  # Change this to your actual Arduino COM port
BAUD = 9600
OUTPUT_FILE = "sensor_data.csv"


def collect_data():
    print("Connecting to Arduino...")

    with serial.Serial(PORT, BAUD, timeout=2) as arduino:
        time.sleep(2)

        with open(OUTPUT_FILE, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "time_ms",
                "temperature_C",
                "smoke_adc",
                "relay_on"
            ])

            print("Collecting sensor data...")
            print("Press Ctrl+C to stop.")

            while True:
                line = arduino.readline().decode(
                    "utf-8", errors="ignore"
                ).strip()

                if not line or line.startswith("time_ms"):
                    continue

                parts = line.split(",")

                if len(parts) != 4:
                    continue

                try:
                    row = [
                        int(parts[0]),
                        float(parts[1]),
                        int(parts[2]),
                        int(parts[3])
                    ]
                except ValueError:
                    continue

                writer.writerow(row)
                file.flush()
                print(row)


try:
    collect_data()

except KeyboardInterrupt:
    print("\nData collection stopped.")

except serial.SerialException as error:
    print("Serial port error:", error)
    print("Check your COM port and close Arduino Serial Monitor.")

finally:
    print("Check sensor_data.csv in your project folder.")
