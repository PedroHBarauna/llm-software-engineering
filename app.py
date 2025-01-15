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

    def handle_chat(history, model_choice, message):
        adapter = on_model_select(model_choice)
        print(message)
        if adapter:
            response = adapter.generate_response(message)
            history.append((message, response))
            return history, ""
        else:
            history.append((message, "Por favor, escolha um modelo primeiro."))
            return history, ""

    with gr.Blocks() as chat_interface:
        gr.Markdown("### Chatbot com Seleção de Modelos")

        with gr.Row():
            model_choice = gr.Dropdown(
                choices=["Local LLM (GPT-NeoX)", "Online LLM (Sabia 3)"],
                label="Escolha o modelo",
            )

        chatbot = gr.Chatbot(label="Chatbot")
        message = gr.Textbox(placeholder="Digite sua mensagem...")

        message.submit(
            handle_chat,
            inputs=[chatbot, model_choice, message],
            outputs=[chatbot, message],
        )

    chat_interface.launch()

if __name__ == "__main__":
    main()
