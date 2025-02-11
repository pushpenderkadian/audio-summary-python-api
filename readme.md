
# Audio Transcription and Summary Generation API

This FastAPI application transcribes an uploaded audio file, generates a summary of the transcription, and provides AI-powered title suggestions. The application uses the Hugging Face API for both transcription (audio-to-text) and summarization.

## Features

- **Audio Transcription:** Converts an audio file into text using the google speech recognition
- **Text Summarization:** Summarizes the transcribed text into key points using the `facebook/bart-large-cnn` model.
- **AI-powered Title Suggestions:** Generates multiple title suggestions based on the summary text using the `mt0-large` model.

## Prerequisites

Before running the application, ensure the following requirements are met:

- Python 3.8 or higher
- `pip` for installing dependencies
- A Hugging Face API token (create one on [Hugging Face](https://huggingface.co)) and store it in a `.env` file or replace directly in the code.

## Installation

1. Clone this repository or download the code to your local machine.

```bash
git clone https://github.com/pushpenderkadian/audio-summary-api.git
cd audio-summary-api
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the `.env` file with your Hugging Face API key:

```env
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

Alternatively, replace `HF_API_TOKEN` in `main.py` and `utils.py` directly with your API key.

## Usage

1. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

2. Open your browser and go to `http://127.0.0.1:8000/docs` to view the auto-generated API documentation and try out the endpoint.

3. To interact with the API:
   - Send a POST request to `/api/generate-summary/` with an audio file (e.g., `.wav` or `.mp3` format) as the body.
   - The response will include the transcription, summary, and AI-generated titles.

### Example API Request

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/generate-summary/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your-audio-file.wav'
```

### Example API Response

```json
{
  "summary": "This is the key point summary of the transcription.",
  "suggested_titles": [
    "A Comprehensive Guide on Transcriptions",
    "Key Insights from the Audio Recording",
    "Audio-to-Text Transcription Overview"
  ],
  "transcription": "This is the transcription of the audio content."
}
```

## Project Structure

```
audio-summary-api/
│
├── main.py                # FastAPI app and endpoint logic
├── utils.py               # Helper functions for API calls
├── .env                   # Hugging Face API key (optional)
├── requirements.txt       # List of dependencies
└── tmp/                   # Temporary storage for uploaded audio files
```

## Dependencies

- `fastapi` for creating the API.
- `requests` for making HTTP requests to Hugging Face APIs.
- `pydantic` for request/response validation.
- `speechrecognition` for audio transcription.
- `python-dotenv` for loading environment variables.

