from llm_adapter import LLMAdapter
import openai
import re

def verificar_somente_numeros(cnpj_str):
    cnpj_numeros = re.sub(r'\D', '', cnpj_str)
    
    if len(cnpj_numeros) == 14:
        return cnpj_numeros
    return None

empresas_mock = {
    "12345678000199": {
        "nome": "Empresa Exemplo LTDA",
        "endereco": "Rua Exemplo, 123, Exemplo City",
        "telefone": "(11) 98765-4321"
    },
    "98765432000188": {
        "nome": "Outra Empresa SA",
        "endereco": "Avenida Teste, 456, Teste Town",
        "telefone": "(21) 12345-6789"
    }
}


def extrair_parte_frase(frase, palavra_chave):
    try:
        index = frase.index(palavra_chave)
        return frase[index + len(palavra_chave):].strip()
    except ValueError:
        return "Palavra-chave não encontrada na frase."
    
def buscar_empresa_por_cnpj(cnpj):
    empresa = empresas_mock.get(cnpj)
    if empresa:
        return empresa
    else:
        return "CNPJ não encontrado."

class OnlineLLMAdapter(LLMAdapter):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None

    def load_model(self):
        print("No local loading required for online model.")
        self.client = openai.OpenAI(api_key=self.api_key, base_url="https://chat.maritaca.ai/api")

    def generate_response(self, prompt: str) -> str:
        if 'devolução' in prompt:
            prompt = 'Pergunte o CNPJ da empresa e fale para digitar apenas números de maneira formal'
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="sabia-3",
                max_tokens=8000
            )
            return response.choices[0].message.content
        else:
            empresa_cnpj = verificar_somente_numeros(prompt)
            if empresa_cnpj:
                    empresa = buscar_empresa_por_cnpj(empresa_cnpj)
                    prompt = f"Diga um tempo de deslocamento para o endereço ficticio {empresa['endereco']} e que será buscado em um dia útil da próxima semana, de maneira formal com atenciosamente Equipe Smartgas no final e utilizando o nome da empresa {empresa['nome']}"
            else:
                empresa = buscar_empresa_por_cnpj(empresa_cnpj)
                prompt = f"Diga um tempo de deslocamento para o endereço ficticio {empresa['endereco']} e que será buscado em um dia útil da próxima semana, de maneira formal com atenciosamente Equipe Smartgas no final e utilizando o nome da empresa {empresa['nome']}"
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="sabia-3",
                max_tokens=8000
            )
            return response.choices[0].message.content