from dotenv import load_dotenv
import openai
import os
import requests

load_dotenv()

endpoint_id = os.environ.get("ENDPOINT_ID")
runpod_base_url = f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1"

# OpenAI client for openai=0.28 might face some issue with openai=1.58.1
openai.api_key = os.environ.get("RUNPOD_API_KEY")
openai.api_base = runpod_base_url

runpod_base_url = f"https://api.runpod.ai/v2/{os.environ.get('ENDPOINT_ID')}/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ.get('RUNPOD_API_KEY')}",
    "Content-Type": "application/json"
}
data = {
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "messages": [{"role": "user", "content": "write a small sarcastic poem on Batman"}],
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 0.95
}

response = requests.post(runpod_base_url, headers=headers, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")

