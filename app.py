import gradio as gr
from local_llm_adapter import LocalLLMAdapter
from online_llm_adapter import OnlineLLMAdapter

def chat_with_model(adapter):
    def chat_function(prompt):
        response = adapter.generate_response(prompt)
        return response

    return chat_function

def main():
    def on_model_select(model_choice):
        if model_choice == "Local LLM (GPT-NeoX)":
            adapter = LocalLLMAdapter(model_name="EleutherAI/gpt-neo-1.3B")
        elif model_choice == "Online LLM (Sabia 3)":
            adapter = OnlineLLMAdapter(api_key="105850918713662678369_8fc1a2cda89a24f5")
        else:
            return None
        adapter.load_model()
        return adapter

    with gr.Blocks() as chat_interface:
        gr.Markdown("### Devolução de Tanques")

        model_choice = gr.Dropdown(
            choices=["Local LLM (GPT-NeoX)", "Online LLM (Sabia 3)"],
            label="Escolha o modelo"
        )

        message = gr.Textbox(placeholder="Digite sua mensagem...", label="Sua pergunta:")
        response = gr.Textbox(label="Resposta:", interactive=False)

        def handle_chat(model_choice, prompt):
            adapter = on_model_select(model_choice)
            if adapter:
                response = adapter.generate_response(prompt)
                return response
            else:
                return "Por favor, escolha um modelo primeiro."

        message.submit(handle_chat, inputs=[model_choice, message], outputs=response)

    chat_interface.launch()

if name == "main":
    main()