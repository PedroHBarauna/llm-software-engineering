from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass