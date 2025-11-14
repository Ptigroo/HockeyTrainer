# Hockey Trainer - .NET Console Client

A simple .NET console application that uploads video files to the Hockey Trainer inference API.

## Prerequisites

- .NET 6.0 SDK or later
- Hockey Trainer API service running (see `services/api/`)

## Quick Start

1. Make sure the API is running:
```bash
cd ../../services/api
python main.py
```

2. Build the client:
```bash
cd examples/dotnet_client
dotnet build
```

3. Run the client:
```bash
# Option 1: Provide video path as argument
dotnet run path/to/video.mp4

# Option 2: Interactive mode (will prompt for path)
dotnet run
```

## Usage Examples

### Command line argument:
```bash
dotnet run ~/videos/hockey_practice.mp4
```

### Interactive mode:
```bash
dotnet run
# Then enter the path when prompted, or drag and drop the file
```

## Features

- ✅ Video file upload to `/infer/video` endpoint
- ✅ API health check before upload
- ✅ Progress indication and file size display
- ✅ JSON response parsing and pretty printing
- ✅ Key metrics extraction and display
- ✅ Error handling and user-friendly messages

## Output Example

```
Hockey Trainer - Video Upload Client
=====================================

Video file: /path/to/video.mp4
API endpoint: http://localhost:8000/infer/video

Connecting to API...
✓ API is healthy

Uploading video...
File size: 15.34 MB
✓ Upload successful

Analysis Results:
=================

{
  "status": "success",
  "filename": "video.mp4",
  "analysis": {
    "ball_tracking": {
      "detected": true,
      "max_speed_kmh": 45.7,
      "avg_speed_kmh": 32.3
    },
    ...
  }
}

--- Key Metrics ---
Max Ball Speed: 45.7 km/h
Ball Detections: 150
Actions Detected: 3
```

## Configuration

To change the API endpoint, edit the `ApiBaseUrl` constant in `Program.cs`:

```csharp
private const string ApiBaseUrl = "http://localhost:8000";
```

## Project Structure

```
examples/dotnet_client/
├── Program.cs                      # Main application code
├── HockeyTrainerClient.csproj     # Project file
└── README.md                       # This file
```

## Building for Distribution

Create a self-contained executable:

```bash
# Windows
dotnet publish -c Release -r win-x64 --self-contained

# macOS
dotnet publish -c Release -r osx-x64 --self-contained

# Linux
dotnet publish -c Release -r linux-x64 --self-contained
```

The executable will be in `bin/Release/net6.0/{runtime}/publish/`

## Troubleshooting

### "Connection error"
- Ensure the API service is running on port 8000
- Check if you can access http://localhost:8000 in a browser

### "Video file not found"
- Verify the file path is correct
- Use absolute paths for best results
- Check file permissions

### "Upload failed: 415"
- The API may not accept that video format
- Try converting to MP4 format

## Dependencies

- System.Text.Json 8.0.5 - JSON serialization/deserialization

## License

Part of the Hockey Trainer project - Personal use
