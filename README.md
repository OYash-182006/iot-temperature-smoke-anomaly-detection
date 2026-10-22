# IoT-Based Temperature and Smoke Monitoring with Machine Learning for Anomaly Detection

## Overview

This project combines an Arduino-based sensor monitoring system with a Python machine learning model to identify potentially unusual temperature and smoke-sensor readings.

The system uses a DS18B20 temperature sensor and an MQ-2 smoke sensor module. Sensor readings are sent to a computer through serial communication. A trained Isolation Forest model analyses temperature and raw smoke-sensor readings and classifies observations as normal or potential anomalies.

## Features

- Real-time temperature monitoring using DS18B20
- Smoke-related readings using an MQ-2 sensor module
- Arduino-to-PC serial communication
- Unsupervised anomaly detection using Isolation Forest
- Model saving and loading with Joblib
- Data collection, inspection, and visualisation
- Streamlit dashboard
- Live anomaly detection using Python

## System Architecture

DS18B20 and MQ-2 Sensors → Arduino Uno → USB Serial Communication → Python Application → Isolation Forest Model → Anomaly Classification and Visualisation

## Hardware Requirements

- Arduino Uno
- DS18B20 temperature sensor
- MQ-2 smoke sensor module
- 5V relay module (optional)
- 4.7 kΩ pull-up resistor for the DS18B20 data line
- Breadboard and jumper wires
- USB cable
- Computer running Python

## Software Requirements

- Python
- Arduino IDE
- Git
- Python libraries listed in `requirements.txt`

## Hardware Connections

| Component | Arduino connection |
|---|---|
| DS18B20 VCC | 5V |
| DS18B20 GND | GND |
| DS18B20 DATA | D3 |
| MQ-2 VCC | 5V |
| MQ-2 GND | GND |
| MQ-2 AO | A0 |
| Relay IN (optional) | D8 |

Connect a 4.7 kΩ pull-up resistor between the DS18B20 DATA line and 5V. Verify the relay module's voltage requirements and trigger polarity before use.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create a virtual environment

Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Project

### Train the anomaly detection model

```bash
python train_model.py
```

This trains the Isolation Forest pipeline and saves the model as `anomaly_model.joblib`.

### Launch the dashboard

```bash
python -m streamlit run app.py
```

### Run live anomaly detection

1. Upload the Arduino sketch to the Arduino Uno.
2. Close the Arduino IDE Serial Monitor.
3. Update the serial port in `live_detect.py` if required.
4. Run:

```bash
python live_detect.py
```

### Collect sensor data

```bash
python collect_data.py
```

Ensure the Arduino is connected to the correct serial port and the baud rate matches the Arduino sketch.

## Machine Learning Methodology

This project uses the Isolation Forest algorithm, an unsupervised machine learning method for identifying unusual observations.

### Input features

- `temperature_C`: temperature measured in degrees Celsius
- `smoke_adc`: raw analogue reading from the MQ-2 sensor

### Model configuration

- Algorithm: Isolation Forest
- Number of estimators: 100
- Contamination parameter: 0.05
- Random state: 42

The contamination parameter controls the model's assumed outlier proportion and decision threshold. It does not represent model accuracy.

Isolation Forest predictions are:
- `1`: normal observation according to the model
- `-1`: potential anomaly according to the model

## Project Structure

```text
ML_Project/
├── app.py
├── collect_data.py
├── train_model.py
├── live_detect.py
├── check_data.py
├── inspect_anamolies.py
├── plot_results.py
├── sensor_data.csv
├── sensor_data_with_results.csv
├── potential_anomalies.csv
├── anomaly_model.joblib
├── temperature_anomalies.png
├── smoke_anomalies.png
├── requirements.txt
├── README.md
└── .gitignore
```

The `.venv/` directory is created locally and should not be committed to GitHub.

## Important Limitations

- The MQ-2 analogue value is a raw sensor reading, not a calibrated smoke concentration in ppm.
- An anomaly is an unusual sensor pattern, not proof of smoke, fire, or a hazardous event.
- The model's output depends on the training data and selected parameters.
- Model accuracy has not been established using a verified labelled test dataset.
- The Python ML model runs on the computer, not directly on the Arduino Uno.
- Relay threshold logic and machine learning anomaly classification are separate functions.

## Safety

This is an educational prototype and is not a certified fire alarm or life-safety system. Do not rely on it for real fire protection. Test only under safe conditions and use the optional relay with low-voltage demonstration loads, not mains-powered equipment or hazardous devices.

## Future Improvements

- Collect a larger and more diverse sensor dataset.
- Validate the model using labelled normal and abnormal samples.
- Evaluate precision, recall, F1-score, and false-alarm rate.
- Add sensor calibration and temporal features.
- Improve dashboard alerts and logging.
- Explore deployment on suitable edge hardware.

## Author

Student Mini-Project — IoT and Machine Learning

## License

Choose an appropriate open-source license before distributing or reusing this project.
