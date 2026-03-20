# 🔍 Log Anomaly Detector

An ML-powered server log analysis tool that detects anomalies in Apache/Nginx logs using **Isolation Forest** — an unsupervised machine learning algorithm that requires no labeled training data.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![ML](https://img.shields.io/badge/ML-Isolation%20Forest-orange)

## 🚀 Features
- Parses real Apache/Nginx access logs
- Detects anomalies using unsupervised ML (no labels needed)
- Explainable results — tells you *why* a line was flagged
- Adjustable sensitivity slider
- Clean dark UI with anomaly score per log line

## 🧠 How It Works
Isolation Forest works by randomly partitioning data — anomalous points
(unusual response times, error spikes, suspicious IPs) are isolated faster
and get a higher anomaly score.

Features used: `response_time`, `status_code`, `bytes`, `hour`, `method`, `path_depth`

## 📁 Project Structure
```
log-anomaly-detector/
├── backend/
│   ├── main.py          # FastAPI app + endpoints
│   ├── detector.py      # Isolation Forest ML model
│   └── log_parser.py    # Apache log parser + feature extraction
├── frontend/
│   └── index.html       # UI — paste logs, see anomalies
├── data/
│   └── sample_logs.txt  # Sample Apache logs for testing
└── requirements.txt
```

## ⚙️ Setup & Run
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/log-anomaly-detector
cd log-anomaly-detector

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the backend
cd backend
uvicorn main:app --reload

# Open the frontend
# Just open frontend/index.html in your browser
```

API docs available at `http://127.0.0.1:8000/docs`

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Scikit-learn
- **ML Model:** Isolation Forest (unsupervised anomaly detection)
- **Frontend:** Vanilla HTML/CSS/JS
- **Log Format:** Apache Combined Log Format
