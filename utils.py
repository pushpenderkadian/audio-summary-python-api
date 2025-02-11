import requests
import os
from dotenv import load_dotenv
load_dotenv()



# Hugging Face API endpoint and token

HF_API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h-lv60-self"
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
HF_SUMMARIZER_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def query_huggingface_api(model_url: str=HF_SUMMARIZER_URL, headers: dict={
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }, payload: dict={}):
    response = requests.post(model_url, headers=headers, json=payload)
    return response.json()


def huggingface_text_generator(prompt):
    API_URL = "https://api-inference.huggingface.co/models/bigscience/mt0-large"
    
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    caption_response = requests.post(API_URL, headers=headers, json={"inputs": f"{prompt}","parameters": {"max_length": 100}},timeout=300)
    if caption_response.status_code != 200:
        return "Title generation failed."
    else:
        caption_response = caption_response.json()
        caption = caption_response[0]["generated_text"]
        return caption
