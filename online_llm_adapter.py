from llm_adapter import LLMAdapter
import openai

class OnlineLLMAdapter(LLMAdapter):
    def init(self, api_key: str):
        self.api_key = api_key
        self.client = None

    def load_model(self):
        print("No local loading required for online model.")
        self.client = openai.OpenAI(api_key=self.api_key, base_url="https://chat.maritaca.ai/api")

    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="sabia-3",
            max_tokens=8000
        )
        return response.choices[0].message.content