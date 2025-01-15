from llm_adapter import LLMAdapter
from transformers import AutoModelForCausalLM, AutoTokenizer

class LocalLLMAdapter(LLMAdapter):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def load_model(self):
        print(f"Loading local model: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def generate_response(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=100, num_return_sequences=1, temperature=0.7)
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        cleaned_output = decoded_output.split("\n")[-1].strip()
        if cleaned_output.startswith("$"):
            cleaned_output = cleaned_output[1:].strip()
        return cleaned_output