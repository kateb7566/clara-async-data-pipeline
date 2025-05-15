# 🌀 Async Data Pipeline

A lightweight, modular, and asynchronous data pipeline built with Python. Designed to ingest external data, transform it in real-time, and store it efficiently using modern Python frameworks.

## ✨ Features

- 🔄 **Asynchronous Ingestion**: Non-blocking data fetching with `httpx` and `asyncio`.
- 🧠 **Smart Transformation**: Customizable transformation logic for parsing, cleaning, and enriching data.
- 🏪 **Pluggable Storage**: Store data using SQL, NoSQL, or file-based solutions.
- 🚀 **FastAPI API Layer**: Expose endpoints for triggering and monitoring the pipeline.
- 🧪 **Test Coverage**: Unit and integration tests for every layer.

## 📁 Project Structure

```bash
async-data-pipeline/
├── app/              # Core pipeline logic
├── tests/            # Unit and integration tests
├── run_pipeline.py   # Optional manual runner
├── README.md
└── requirements.txt
