# 🤖 Terminal-Bot - Chatbot Inteligente

Um chatbot inteligente desenvolvido em Python que oferece duas interfaces: uma versão web moderna com **Streamlit** e uma versão de linha de comando para uso em terminal.

## 📋 Descrição

Terminal-Bot é um assistente conversacional alimentado pela **API Groq** e **LangChain**, capaz de fornecer respostas inteligentes e contextualizadas. O projeto oferece funcionalidades avançadas como:

- 💬 Conversas fluidas em tempo real
- 🔍 Busca na web integrada (DuckDuckGo)
- 📄 Processamento e análise de documentos PDF
- 🧠 Embeddings semânticos com transformers
- 📚 Armazenamento vetorial local com FAISS
- 👁️ Análise de imagens com visão computacional

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- Chave API da [Groq](https://console.groq.com)

### Instalação

1. **Clone ou baixe o projeto**
   ```bash
   cd Terminal-Bot
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a variável de ambiente**
   
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   GROQ_API_KEY=sua_chave_api_aqui
   ```

## 🎮 Uso

### Interface Web (Streamlit)

Execute a aplicação web:
```bash
streamlit run app.py
```

A aplicação abrirá no navegador em `http://localhost:8501`

**Funcionalidades:**
- Interface amigável com bate-papo em tempo real
- Upload de arquivos PDF para análise
- Upload de imagens para visão computacional
- Busca integrada na web
- Histórico de conversas

### Interface de Terminal

Execute o chatbot no terminal:
```bash
python chatbot_terminal.py
```

**Uso:**
```
🤖 Chatbot iniciado! (digite 'sair' para encerrar)

Você: Olá, como você pode me ajudar?
Bot: Olá! Sou um assistente útil e estou aqui para ajudá-lo...

Você: sair
👋 Até mais!
```

**Comandos:**
- Digite sua mensagem e pressione Enter
- Digite `sair`, `exit` ou `quit` para encerrar
- Pressione Ctrl+C para interromper

## 📦 Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `streamlit` | - | Framework para interface web |
| `python-dotenv` | - | Gerenciamento de variáveis de ambiente |
| `langchain-core` | - | Core do LangChain |
| `langchain-community` | - | Integrações comunitárias do LangChain |
| `langchain-groq` | - | Integração com API Groq |
| `duckduckgo-search` | - | Busca na web |
| `pymupdf` | - | Processamento de PDFs |
| `groq` | - | Cliente oficial da API Groq |
| `faiss-cpu` | - | Busca vetorial local |
| `langchain-text-splitters` | - | Divisão de textos |
| `langchain-huggingface` | - | Embeddings com HuggingFace |
| `sentence-transformers` | - | Modelos de transformers para embeddings |

## 🏗️ Estrutura do Projeto

```
Terminal-Bot/
├── app.py                      # Interface web com Streamlit
├── chatbot_terminal.py         # Interface de terminal
├── requirements.txt            # Dependências do projeto
├── teste.py                    # Testes e experimentos
└── README.md                   # Este arquivo
```

## 🔑 Configuração da API Groq

1. Acesse [console.groq.com](https://console.groq.com)
2. Faça login ou crie uma conta
3. Crie uma nova chave API
4. Adicione a chave ao arquivo `.env`

## 🎯 Modelos Disponíveis

- **LLM Principal**: `openai/gpt-oss-20b` (Groq)
- **Embeddings**: `all-MiniLM-L6-v2` (HuggingFace)
- **Temperatura**: 0.7 (criatividade moderada)

## 🐛 Troubleshooting

### Erro: "GROQ_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme que a chave API está corretamente definida
- Reinicie a aplicação

### Erro: "Modelos de embeddings não carregados"
- Certifique-se de que a internet está conectada (primeira execução baixa os modelos)
- Verifique o espaço em disco disponível

### Aplicação Streamlit não abre
- Verifique se a porta 8501 não está em uso
- Tente: `streamlit run app.py --server.port 8502`

## 📝 Exemplo de Uso Programático

```python
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

chat = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=api_key
)

mensagens = [
    SystemMessage(content="Você é um assistente útil.")
]

resposta = chat.invoke([
    *mensagens,
    HumanMessage(content="Qual é a capital do Brasil?")
])

print(resposta.content)
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📄 Licença

Este projeto é de código aberto. Verifique o arquivo LICENSE para mais detalhes.

## 🔗 Links Úteis

- [Groq API Docs](https://console.groq.com/docs)
- [LangChain Docs](https://python.langchain.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [FAISS Docs](https://faiss.ai/)

## 📞 Suporte

Caso tenha dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Python, LangChain e Groq**
