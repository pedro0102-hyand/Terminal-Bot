import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Inicializa o modelo da Groq usando a API OpenAI-compatible
chat = ChatOpenAI(
    temperature=0.7,
    model="llama3-8b-8192",  # ou outro modelo disponível na Groq
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Mensagens de contexto
mensagens = [
    SystemMessage(content="Você é um assistente útil e direto.")
]

# Loop do terminal
print("🤖 Chatbot iniciado! (digite 'sair' para encerrar)\n")

while True:
    entrada = input("Você: ")
    if entrada.lower() in ["sair", "exit", "quit"]:
        print("👋 Até mais!")
        break

    mensagens.append(HumanMessage(content=entrada))
    resposta = chat.invoke(mensagens)
    mensagens.append(resposta)
    print(f"Bot: {resposta.content}\n")

