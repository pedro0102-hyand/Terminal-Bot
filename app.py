import os
import base64
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from groq import Groq
import fitz

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Carrega as variáveis de ambiente do arquivo .env
if not api_key:
    st.error("❌ Erro: GROQ_API_KEY não encontrada no arquivo .env ou nas variáveis de ambiente.")
    st.stop()

# configuração da página web
st.set_page_config(page_title="Chatbot Terminal", page_icon="🤖", layout="centered")

# variável para armazenar a imagem
imagem_base64 = None
imagem_tipo = None

# modelo de visão para análise de imagens
vision_client = Groq(api_key = api_key)

# sidebar
with st.sidebar:

    # configurações do chatbot
    st.header("Configurações")
    temperatura = st.slider("Temperatura do modelo", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="A temperatura controla a aleatoriedade das respostas do modelo.")
    st.divider()

    # anexar arquivo
    st.header("Anexar Arquivo")
    arquivo = st.file_uploader("Escolha um arquivo para anexar (opcional)", type=["txt", "pdf", "png", "jpg", "jpeg"])
    texto_arquivo = ""

    if arquivo is not None:

        # exibe informações do arquivo
        st.success("Arquivo anexado com sucesso!")
        tamanho_mb = arquivo.size / (1024 * 1024)
        st.write(f"**Nome:** {arquivo.name}")
        st.write(f"**Tipo:** {arquivo.type}")
        st.write(f"**Tamanho:** {tamanho_mb:.2f} MB")

        if arquivo.type == "application/pdf":

            # ler o arquivo PDF
            st.write("📄 PDF detectado.")
            dados = arquivo.read()
            documento = fitz.open(stream=dados, filetype="pdf")
            texto = "".join(pagina.get_text() for pagina in documento)

            # verifica se o PDF contém texto pesquisável
            if texto.strip():
                texto_arquivo = texto
                st.success("✅ Texto extraído com sucesso!")

            else:

                # PDF escaneado detectado: executa OCR página por página via Qwen
                st.info("🔍 PDF digitalizado detectado. Executando OCR com Qwen...")
                with st.spinner("Extraindo texto das páginas digitalizadas..."):

                    textos_ocr = [] # lista para armazenar o texto extraído de cada página

                    for num_pag, pagina in enumerate(documento):
                        # Renderiza a página do PDF em imagem (150 DPI para bom equilíbrio de clareza/tamanho)
                        pix = pagina.get_pixmap(dpi=150)
                        img_bytes = pix.tobytes("png")

                        # Converte a imagem para base64 para enviar ao modelo de visão
                        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

                        # Chama o Qwen para transcrever a página
                        resp_ocr = vision_client.chat.completions.create(
                            model="qwen/qwen3.6-27b",
                            temperature=0.3,
                            messages=[
                                {
                                    "role": "system",
                                    "content": "Você é um motor de OCR de alta precisão. Transcreva fielmente todo o conteúdo legível (tabelas em Markdown, títulos e textos). Não adicione saudações nem comentários."
                                },
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": "Transcreva todo o conteúdo desta página de documento:"},
                                        {
                                            "type": "image_url",
                                            "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                                        }
                                    ]
                                }
                            ]
                        )
                        textos_ocr.append(f"--- Página {num_pag + 1} ---\n{resp_ocr.choices[0].message.content}")

                    texto_arquivo = "\n\n".join(textos_ocr)
                    st.success("✅ OCR das páginas concluído com sucesso!")

            documento.close()

        elif arquivo.type == "text/plain":

            # ler o arquivo TXT
            st.write("📄 Arquivo TXT detectado.")
            texto = arquivo.read().decode("utf-8")
            texto_arquivo = texto

            if not texto.strip():
                st.warning("⚠️ O arquivo TXT está vazio.")

        elif arquivo.type in ["image/png", "image/jpeg"]:
            
            st.write("🖼️ Imagem detectada.")
            st.image(arquivo, caption=arquivo.name)

            # converte a imagem para base64 para enviar ao modelo de visão
            imagem_bytes = arquivo.getvalue()
            imagem_base64 = base64.b64encode(imagem_bytes).decode("utf-8")
            imagem_tipo = arquivo.type

        st.divider()

    # limpar conversa
    if st.button("Limpar Conversa", use_container_width=True):
        st.session_state.mensagens = [SystemMessage(content="Você é um assistente útil, inteligente e direto.")]
        st.rerun()

# modelo de linguagem para conversas de texto
chat = ChatGroq(model = "openai/gpt-oss-20b", temperature = temperatura, api_key = api_key)

# memoria de mensagens do chatbot
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [SystemMessage(content="Você é um assistente útil, inteligente e direto.")]

# interface do chatbot
st.title("🤖 Chatbot Terminal")
st.caption("Digite sua mensagem abaixo e pressione Enter para enviar.")

# histórico de mensagens
for mensagem in st.session_state.mensagens:

    # mensagens do usuário
    if isinstance(mensagem, HumanMessage):
        with st.chat_message("user"):
            st.markdown(f"**Você:** {mensagem.content}")

    # mensagens do sistema (bot)
    elif isinstance(mensagem, AIMessage):
        with st.chat_message("assistant"):
                st.markdown(f"**Bot:** {mensagem.content}")

# entrada do usuário
entrada = st.chat_input("Digite sua mensagem aqui...")

if entrada:

    # adiciona a mensagem do usuário ao histórico
    mensagem_usuario = HumanMessage(content=entrada)
    st.session_state.mensagens.append(mensagem_usuario)
    with st.chat_message("user"): st.markdown(f"**Você:** {entrada}")

    try:
        with st.chat_message("assistant"):
            with st.spinner("O bot está pensando..."):

                # imagem → Qwen-3.6-27B
                if imagem_base64:
                    resposta_vision = vision_client.chat.completions.create(

                        model = "qwen/qwen3.6-27b",
                        temperature = 0.3,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Você é um motor de OCR de alta precisão. Sua tarefa é transcrever e extrair "
                                    "com máxima fidelidade todo o conteúdo textual e estruturado presente na imagem.\n"
                                    "- Preserve a hierarquia original (títulos, subtítulos e listas).\n"
                                    "- Converta tabelas presentes na imagem diretamente para formato de tabela em Markdown.\n"
                                    "- Se houver recibos, notas ou formulários, capture pares de chave/valor com exatidão.\n"
                                    "- Não invente dados ilegíveis; se um trecho estiver ilegível, indique com [ilegível].\n"
                                    "- Responda à instrução do usuário priorizando a exatidão dos dados transcritos."
                                )
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": entrada
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": (
                                                f"data:{imagem_tipo};"
                                                f"base64,{imagem_base64}"
                                            )
                                        }
                                    }
                                ]
                            }
                        ]
                    )

                    resposta_texto = (resposta_vision.choices[0].message.content)
                    st.markdown(f"**Bot:** {resposta_texto}")

                    # salva a resposta no histórico
                    st.session_state.mensagens.append(AIMessage(content=resposta_texto))

                else:

                    # copia das mensagens para enviar ao modelo de linguagem
                    mensagens_para_llm = (st.session_state.mensagens.copy())

                    if texto_arquivo.strip():

                        # prompt para fornecer contexto do arquivo ao modelo de linguagem
                        contexto_arquivo = SystemMessage(content=f"""Você está respondendo a perguntas sobre um arquivo fornecido pelo usuário. Utilize o conteúdo do arquivo abaixo como contexto para responder. CONTEÚDO DO ARQUIVO: {texto_arquivo} Responda utilizando as informações presentes no arquivo. Se a informação solicitada não estiver presente no arquivo, informe claramente que ela não foi encontrada no documento. """)
                        mensagens_para_llm.insert(1,contexto_arquivo)

                    # envia as mensagens para o modelo de linguagem e obtém a resposta
                    resposta = chat.invoke(mensagens_para_llm)
                    st.session_state.mensagens.append(AIMessage(content=resposta.content))
                    st.markdown(f"**Bot:** {resposta.content}")

    except Exception as e:
        st.error( f"❌ Ocorreu um erro ao processar " f"a resposta: {e}")
        st.session_state.mensagens.pop()

