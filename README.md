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



Why Fail-Open?

The check_velocity logic is wrapped in a try/except block. If the Redis/Memurai database goes offline, the system defaults to allowing the transaction. In a banking context, Availability often takes precedence over strict security checks to prevent service outages for legitimate customers.

