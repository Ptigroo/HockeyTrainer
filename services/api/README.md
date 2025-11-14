# HockeyTrainer - Inference API (starter)

This folder contains a minimal FastAPI-based inference service and Docker setup for prototyping:
- main.py: FastAPI app with /health and /infer/video endpoints
- requirements.txt: Python deps
- Dockerfile: builds a simple container

Usage (local):
1. Create a Python venv and install requirements:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run the app:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

The /infer/video endpoint accepts multipart/form-data file upload (field name: "file") and returns a JSON stub.
Replace the placeholder inference code in `run_inference_on_video` with your detector/pose/event pipeline.
