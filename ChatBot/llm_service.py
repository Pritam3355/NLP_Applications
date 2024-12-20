import os
from together import Together
from groq import Groq

class LLMService:
    def __init__(self, api_service="Groq"):
        self.api_service = api_service
        self.api_keys = {
            "Together": os.environ.get('TOGETHER_API_KEY'),
            "Groq": os.environ.get("GROQ_API_KEY")
        }

    def generate_response(self, conversation_history):
        if self.api_service == "Together":
            client = Together(api_key=self.api_keys["Together"])
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
                messages=conversation_history,
                max_tokens=512,
                temperature=0.3,
                top_p=0.7,
                stop=["<|eot_id|>", "<|eom_id|>"],
                stream=False
            )
        else:
            client = Groq(api_key=self.api_keys["Groq"])
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=conversation_history,
                max_tokens=1024,
                temperature=0.3,
                top_p=0.7,
                stop=["<|eot_id|>", "<|eom_id|>"],
                stream=False
            )
        return response.choices[0].message.content
