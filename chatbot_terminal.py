import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ Erro: GROQ_API_KEY não encontrada no arquivo .env ou nas variáveis de ambiente.")
    sys.exit(1)

chat = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=api_key
)

mensagens = [
    SystemMessage(content="Você é um assistente útil, inteligente e direto.")
]

print("🤖 Chatbot iniciado! (digite 'sair' para encerrar)\n")

while True:
    try:
        entrada = input("Você: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Até mais!")
        break

    if not entrada:
        continue

    if entrada.lower() in ["sair", "exit", "quit"]:
        print("👋 Até mais!")
        break

    mensagens.append(HumanMessage(content=entrada))
    
    try:
        resposta = chat.invoke(mensagens)
        mensagens.append(resposta)
        print(f"\nBot: {resposta.content}\n")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao processar a resposta: {e}\n")
        mensagens.pop()