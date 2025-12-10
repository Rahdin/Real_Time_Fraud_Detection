# Real-Time Transaction Fraud Detection Engine
A high-performance, asynchronous fraud detection microservice built with FastAPI, Redis, and Scikit-Learn.

This system processes financial transactions in real-time, applying a two-layer defense strategy:

Deterministic Rules: Velocity checks (rate limiting) using Redis to flag high-frequency transaction attempts.

Probabilistic AI: An Unsupervised Machine Learning model (Isolation Forest) to detect mathematical anomalies in transaction patterns.

🚀 Key Features
Real-Time Latency: Sub-100ms response times using asynchronous Python (async/await).

Hybrid Analysis: Combines stateful velocity tracking (Redis) with stateless ML inference.

Fail-Open Architecture: Designed for high availability; system degrades gracefully if the ML model or database becomes unreachable.

Data Validation: Strict schema enforcement using Pydantic.

🛠️ Tech Stack
Framework: Python 3.9+, FastAPI

Database (Cache): Redis (via Memurai for Windows)

Machine Learning: Scikit-Learn (Isolation Forest)

Server: Uvicorn (ASGI)

🏗️ Architecture
The request flow is as follows:

Client sends a transaction via POST request.

FastAPI validates the data schema.

Velocity Check: The app queries Memurai (Redis-compatible store) to ensure the user hasn't exceeded 3 transactions per minute.

Anomaly Check: The app passes the data to the Isolation Forest model to detect outliers.

Response: A JSON verdict is returned (is_fraud: true/false).

💻 Setup & Installation (Windows)
This project uses Memurai as a drop-in replacement for Redis on Windows.

Prerequisites
Python 3.9+ installed.

Memurai Developer Edition installed and running.

Download: https://www.memurai.com/get-memurai

Verify installation by running memurai-cli ping in cmd.

Step 1: Clone & Configure
Bash

git clone https://github.com/YOUR_USERNAME/fraud-engine.git
cd Real_Time_Fraud_Detection

# Create virtual environment
python -m venv venv

# Activate environment
# PowerShell:
.venv\Scripts\activate
# Command Prompt:
venv\Scripts\activate.bat

Step 2: Install Dependencies

Bash

pip install -r requirements.txt

Step 3: Train the ML Model

Before running the API, you must generate the Isolation Forest model artifact. This 

script simulates banking transactions to train the "brain."

Bash

python -m scripts.train_model



Step 4: Start the Server

Bash

uvicorn app.main:app --reload

The API will be live at http://127.0.0.1:8000

🔌 API Usage
You can test the API using the auto-generated Swagger UI or via curl/PowerShell.

Interactive UI: Go to http://localhost:8000/docs

Test Case 1: Safe Transaction

A low amount transaction ($45) from a trusted merchant.

PowerShell

# PowerShell Command
curl.exe -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d "{\"transaction_id\": \"safe_1\", \"user_id\": \"bob\", \"amount\": 45.00, \"merchant_id\": \"amazon\", \"merchant_risk_score\": 5}"

Response:

JSON

{
  "is_fraud": false,
  "risk_score": 0.05,
  "reason": []
}

Test Case 2: ML Anomaly

A high-value transaction ($2500+) that deviates from the training distribution.

PowerShell

# PowerShell Command
curl.exe -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d "{\"transaction_id\": \"bad_1\", \"user_id\": \"hacker\", \"amount\": 2500.00, \"merchant_id\": \"sketchy_site\", \"merchant_risk_score\": 80}"

Response:

JSON

{
  "is_fraud": true,
  "risk_score": 0.95,
  "reason": ["ML_ANOMALY_DETECTED"]
}

Test Case 3: Velocity Attack

Run the "Safe Transaction" command 4 times in quick succession.

Response (4th attempt):

JSON

{
  "is_fraud": true,
  "reason": ["HIGH_VELOCITY_TRIGGER"]
}

🧠 Design Decisions

Why Isolation Forest?

I chose Isolation Forest over distance-based algorithms (like KNN) or supervised models because:

Unsupervised: It detects "unknown unknowns" (new fraud patterns) without needing labeled historical data.

Efficiency: It runs in linear time O(n), making it suitable for high-throughput payment processing.

Imbalanced Data: It excels at identifying rare outliers (fraud) in massive datasets of normal behavior.

Why Fail-Open?

The check_velocity logic is wrapped in a try/except block. If the Redis/Memurai database goes offline, the system defaults to allowing the transaction. In a banking context, Availability often takes precedence over strict security checks to prevent service outages for legitimate customers.

