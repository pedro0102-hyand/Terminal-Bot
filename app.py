import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import fitz 

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

    # configuracoes do chatbot
    st.header("Configurações")
    temperatura = st.slider("Temperatura do modelo", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="A temperatura controla a aleatoriedade das respostas do modelo. Valores mais baixos resultam em respostas mais determinísticas, enquanto valores mais altos produzem respostas mais variadas.")
    st.divider()

    # anexar arquivo
    st.header("Anexar Arquivo")
    arquivo = st.file_uploader("Escolha um arquivo para anexar (opcional)", type=["txt", "pdf"])

    texto_arquivo = ""

    # exibe informações do arquivo anexado
    if arquivo is not None:

        st.success("Arquivo anexado com sucesso!")
        tamanho_mb = arquivo.size / (1024 * 1024)
        st.write(f"**Nome:** {arquivo.name}")
        st.write(f"**Tipo:** {arquivo.type}")
        st.write(f"**Tamanho:** {tamanho_mb:.2f} MB")

        # tratamento para arquivos PDF
        if arquivo.type == "application/pdf":

            # abrindo o arquivo PDF usando PyMuPDF
            st.write("📄 PDF detectado.")
            dados = arquivo.read()
            documento = fitz.open(stream = dados , filetype = "pdf")

            # extrair texto do pdf
            texto = ""
            for pagina in documento:
                texto += pagina.get_text()
            documento.close()
            texto_arquivo = texto

            if not texto.strip():
                st.warning("⚠️ O PDF não contém texto extraível. Ele pode ser uma imagem ou protegido contra cópia.")

        # tratamento para arquivos TXT
        if arquivo.type == "text/plain":

            texto = arquivo.read().decode("utf-8")
            texto_arquivo = texto

            if not texto.strip():
                st.warning("⚠️ O arquivo TXT está vazio.")

        st.divider()

    # limpar conversa
    if st.button("Limpar Conversa", use_container_width=True):
        st.session_state.mensagens = [
            SystemMessage(content="Você é um assistente útil, inteligente e direto.")
        ]
        st.rerun()

# modelo de llm
chat = ChatGroq(model="openai/gpt-oss-20b", temperature=temperatura, api_key=api_key)

# memoria da conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [ SystemMessage(content="Você é um assistente útil, inteligente e direto.") ]

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

                # Cria uma cópia das mensagens para enviar à LLM, incluindo o contexto do arquivo se houver
                mensagens_para_llm = st.session_state.mensagens.copy()

                if texto_arquivo.strip(): # strip remove espaços em branco no início e no final do texto

                    # Adiciona o conteúdo do arquivo como contexto para a LLM
                    contexto_arquivo = SystemMessage(content=f"Você está respondendo a perguntas sobre um arquivo fornecido pelo usuário.\n\nUtilize o conteúdo do arquivo abaixo como contexto para responder.\n\nCONTEÚDO DO ARQUIVO:\n{texto_arquivo}\n\nResponda utilizando as informações presentes no arquivo.\nSe a informação solicitada não estiver presente no arquivo,\ninforme claramente que ela não foi encontrada no documento.")
                    mensagens_para_llm.insert(1, contexto_arquivo) # Insere o contexto do arquivo logo após a mensagem do sistema inicial

                resposta = chat.invoke(mensagens_para_llm)
                st.session_state.mensagens.append(resposta)
                st.markdown(f"**Bot:** {resposta.content}")

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao processar a resposta: {e}")
        st.session_state.mensagens.pop()

