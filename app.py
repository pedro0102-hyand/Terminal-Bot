import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Carrega as variáveis de ambiente do arquivo .env
if not api_key:
    st.error("❌ Erro: GROQ_API_KEY não encontrada no arquivo .env ou nas variáveis de ambiente.")
    st.stop()

# configuracao da pagina web
st.set_page_config(page_title="Chatbot Terminal", page_icon="🤖", layout="centered")

# sidebar
with st.sidebar:
    st.header("Configurações")
    temperatura = st.slider("Temperatura do modelo", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
    st.divider()
    if st.button("Limpar Conversa", use_container_width=True):
        st.session_state.mensagens = [
            SystemMessage(content="Você é um assistente útil, inteligente e direto.")
        ]
        st.rerun()


# modelo de llm
chat = ChatGroq(

    model="openai/gpt-oss-20b",
    temperature=temperatura,
    api_key=api_key

)

# memoria da conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        SystemMessage(content="Você é um assistente útil, inteligente e direto.")
    ]

# interface do chatbot
st.title("🤖 Chatbot Terminal")
st.caption("Digite sua mensagem abaixo e pressione Enter para enviar. Digite 'sair' para encerrar a conversa.")

# histórico de mensagens
for mensagem in st.session_state.mensagens :

    # exibe a mensagem do usuário 
    if isinstance(mensagem, HumanMessage):
        with st.chat_message("user"):
            st.markdown(f"**Você:** {mensagem.content}")

    # exibe a mensagem do bot
    elif mensagem.type == "ai" :
        with st.chat_message("assistant"):
            st.markdown(f"**Bot:** {mensagem.content}")

# entrada do usuário
entrada = st.chat_input("Digite sua mensagem aqui...")

if entrada:

    # mensagem do usuário
    mensagem_usuario = HumanMessage(content=entrada)
    st.session_state.mensagens.append(mensagem_usuario)

    with st.chat_message("user"):
        st.markdown(f"**Você:** {entrada}")

    # resposta do bot
    try:
        with st.chat_message("assistant"):
            with st.spinner("O bot está pensando..."):
                resposta = chat.invoke(st.session_state.mensagens)
                st.session_state.mensagens.append(resposta)
                st.markdown(f"**Bot:** {resposta.content}")

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao processar a resposta: {e}")
        st.session_state.mensagens.pop()


