from together import Together
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_service = os.environ.get('API_USE')
        self.api_keys = {
            "Together": os.environ.get('TOGETHER_API_KEY'),
            "Groq": os.environ.get("GROQ_API_KEY"),
            "RunPod": os.environ.get("RUNPOD_API_KEY")
        }

    def generate_response(self, conversation_history):
        response = None  # Avoid UnboundLocalError
        if self.api_service == "Together":
            client = Together(api_key=self.api_keys["Together"])
            response = client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=conversation_history,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.95,
                stop=["[/INST]", "</s>"],
                stream=False
            )
        elif self.api_service == "Groq":
            client = Groq(api_key=self.api_keys["Groq"])
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=conversation_history,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.7,
                stop=["<|eot_id|>", "<|eom_id|>"],
                stream=False
            )
        else:
            raise ValueError(f"Unsupported API: {self.api_service}")

        if not response or not hasattr(response, "choices"):
            raise ValueError("Invalid response")
        return response.choices[0].message.content
