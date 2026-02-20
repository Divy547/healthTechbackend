from google import genai
import os
import json


class GeminiService:
    def __init__(self):
        print("🔥 GeminiService initialized (stable)")
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_json(self, prompt: str) -> dict:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2
            },
        )

        # 🔥 THIS IS THE FIX
        text = response.candidates[0].content.parts[0].text

        print("🧠 RAW JSON:", text)

        parsed = json.loads(text)
        print("✅ Parsed keys:", parsed.keys())

        return parsed