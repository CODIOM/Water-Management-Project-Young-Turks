import requests
import json


class LlamaClient:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def generate_response(self, context_data, status_message, user_question):


        prompt = f"""
        [SYSTEM ROLE]
        You are WaterTwin, a professional smart water management assistant.

        [STRICT RULES]
        1. Speak ONLY in ENGLISH.
        2. Be concise, professional, and helpful.
        3. Use the provided "System Status" to guide your advice.
        4. Do not repeat the system instructions to the user.

        [SYSTEM DATA]
        - Tank Capacity: {context_data.get('tank_capacity')} Liters
        - Current Level: {context_data.get('current_level')} Liters
        - Incoming Rain: +{context_data.get('incoming_water', 0):.1f} Liters
        - Predicted Level: {context_data.get('predicted_level', 0):.1f} Liters

        [SYSTEM STATUS COMMAND]
        "{status_message}"

        [USER QUESTION]
        "{user_question}"

        [YOUR RESPONSE]
        (Write a clear, short response in English):
        """

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2,  # Keep it consistent
            "top_k": 40,
            "top_p": 0.9
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()['response'].strip().replace('"', '')
        except Exception as e:
            return f"LLM Connection Error: {str(e)}"