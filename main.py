import os
import requests
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import tempfile
import speech_recognition as sr

from utils import query_huggingface_api, huggingface_text_generator,HF_API_TOKEN

app = FastAPI()

# Pydantic model for the output
class SummaryResponse(BaseModel):
    summary: str
    suggested_titles: list
    transcription: str


@app.post("/api/generate-summary/", response_model=SummaryResponse)
async def generate_summary(file: UploadFile = File(...)):
    # Create a temporary file to store the uploaded audio
    
    with open(f'./tmp/{file.filename}', "wb") as buffer:
        buffer.write(await file.read())
    recognizer = sr.Recognizer()

    # Prepare headers for Hugging Face API requests
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }

    # 1. Transcribe the audio (Audio-to-Text with Speaker Diarization)
    transcription_payload = {
        "inputs": f'./tmp/{file.filename}',
    }
    print(transcription_payload)
    with sr.AudioFile(f'./tmp/{file.filename}') as source:
        audio_data = recognizer.record(source)

    # Recognize the speech using Google's speech recognition
    try:
        transcription_text = recognizer.recognize_google(audio_data)
        print("Transcription: ", transcription_text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")

    # 2. Summarize the transcription (Key Point Summarization)
    summarization_payload = {
        "inputs": transcription_text,
    }

    summarization_response = query_huggingface_api(HF_SUMMARIZER_URL, headers, summarization_payload)
    summary_text = summarization_response[0].get("summary_text", "Summary generation failed.")

    # 3. Generate AI-powered titles (Title Suggestions)
    title1= huggingface_text_generator(f'write a title based on this summary : {summary_text}')
    title2= huggingface_text_generator(f'write a title based on this summary other then {title1}: {summary_text}')
    title3=huggingface_text_generator(f'write a title based on this summary other then {title1} and {title2}: {summary_text}')

    titles = [
        title1,
        title2,
        title3
    ]

    # Clean up temporary files

    return SummaryResponse(
        summary=summary_text,
        suggested_titles=titles,
        transcription=transcription_text
    )


