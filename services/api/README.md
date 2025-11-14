# Hockey Trainer - Inference API Service

A minimal FastAPI service for video inference with Docker support.

## Overview

This is a **starter template** for the Hockey Trainer inference service. It provides:
- A FastAPI REST API with a `/infer/video` endpoint
- Video file upload handling
- Placeholder inference results
- Docker containerization

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python main.py
```
or
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Using Docker

1. Build the image:
```bash
docker build -t hockey-trainer-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 hockey-trainer-api
```

3. Access the API at http://localhost:8000

## API Endpoints

### `GET /`
Health check endpoint

**Response:**
```json
{
  "service": "Hockey Trainer Inference API",
  "status": "running",
  "version": "0.1.0"
}
```

### `GET /health`
Detailed health check

### `POST /infer/video`
Upload a video for analysis

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: video file

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/infer/video" \
  -F "file=@/path/to/video.mp4"
```

**Response:**
```json
{
  "status": "success",
  "filename": "video.mp4",
  "analysis": {
    "ball_tracking": {
      "detected": true,
      "max_speed_kmh": 45.7,
      "avg_speed_kmh": 32.3,
      "detections_count": 150
    },
    "action_recognition": {
      "actions_detected": [...]
    },
    "posture_analysis": {
      "postures": [...]
    }
  }
}
```

## Next Steps: Replacing Placeholder Inference

The current implementation returns **placeholder results**. To integrate real inference:

1. **Add OpenCV and dependencies** to `requirements.txt`:
```
opencv-python==4.8.1.78
numpy==1.24.3
mediapipe==0.10.7
```

2. **Import existing modules** in `main.py`:
```python
import sys
sys.path.append('../../')  # Add project root to path
from ball_tracking_video import BallTrackerVideo
from action_recognition import ActionRecognizer
from posture_detection import PostureDetector
```

3. **Replace placeholder logic** in the `/infer/video` endpoint:
```python
# Instead of placeholder results, use:
tracker = BallTrackerVideo(temp_path)
results = tracker.analyze_video()

# Process with action recognition
recognizer = ActionRecognizer()
actions = recognizer.analyze(temp_path)

# Add posture analysis
posture_detector = PostureDetector()
postures = posture_detector.analyze(temp_path)
```

4. **Return actual results** from the analysis

## Testing

Test the API with the .NET client in `examples/dotnet_client/` or use curl:

```bash
# Upload a test video
curl -X POST "http://localhost:8000/infer/video" \
  -F "file=@test_video.mp4" \
  | jq .
```

## Environment Variables

Currently no environment variables are required. For production, consider adding:
- `LOG_LEVEL`: Logging level (default: INFO)
- `MAX_FILE_SIZE`: Maximum upload size
- `TEMP_DIR`: Temporary file directory

## Production Deployment

For production:
1. Use a proper ASGI server configuration
2. Add authentication/authorization
3. Implement rate limiting
4. Add monitoring and logging
5. Use a reverse proxy (nginx)
6. Configure CORS if needed
7. Set up proper file cleanup

## Architecture

```
services/api/
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
├── Dockerfile       # Container definition
└── README.md        # This file
```

## License

Part of the Hockey Trainer project - Personal use
