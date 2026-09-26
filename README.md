# 🤖 Terminal-Bot

Chatbot multimodal em Python com interface web em Streamlit, usando Groq, LangChain, embeddings, RAG e visão computacional.

## Visão geral

Este projeto funciona como um assistente conversacional que pode:

- responder em texto usando um LLM da Groq;
- pesquisar na web com DuckDuckGo;
- processar arquivos `.txt` e `.pdf` via RAG;
- analisar imagens com um modelo de visão;
- extrair texto de PDFs digitalizados por OCR;
- indexar documentos em um banco vetorial local com FAISS;
- recuperar trechos semanticamente relevantes para responder melhor.

A aplicação principal está em [app.py](app.py). O projeto ainda contém um arquivo de teste em [teste.py](teste.py).

## Arquitetura do projeto

O sistema é composto por 3 motores principais:

1. LLM principal
   - Modelo: `openai/gpt-oss-20b`
   - Biblioteca: `langchain_groq`
   - Função: geração final da resposta conversacional

2. Modelo de visão
   - Modelo: `qwen/qwen3.6-27b`
   - Biblioteca: `groq`
   - Função: analisar imagens e fazer OCR em PDFs digitalizados

3. Embeddings + busca vetorial
   - Modelo: `all-MiniLM-L6-v2`
   - Biblioteca: `langchain_huggingface` + `FAISS`
   - Função: transformar textos em vetores e recuperar contexto semântico por RAG

## Fluxos implementados

### 1) Fluxo de conversa normal

Quando o usuário envia uma mensagem normal, sem imagem e sem documento anexado:

- a mensagem entra no histórico da sessão;
- o app monta `mensagens_para_llm`;
- envia para o LLM principal;
- retorna a resposta final.

Esse é o fluxo mais simples do chatbot.

### 2) Fluxo de busca na web

Quando a opção de busca na web está ativada:

- a entrada do usuário é enviada para DuckDuckGo;
- o app recebe resultados com `snippet` e `link`;
- esses resultados são convertidos em contexto em texto;
- esse contexto é inserido na lista de mensagens antes do LLM;
- o modelo responde com base nessas fontes externas.

Esse é um fluxo de contexto em tempo real, diferente do RAG.

### 3) Fluxo de RAG com documento local

Quando um arquivo `.txt` ou um PDF textual é anexado:

- o texto é extraído;
- o conteúdo é fragmentado em chunks;
- os chunks são convertidos em embeddings;
- são armazenados em um banco vetorial FAISS;
- quando o usuário pergunta algo, o sistema busca os trechos mais relevantes;
- esses trechos são passados ao LLM como contexto;
- o modelo responde usando somente o conteúdo relevante do documento.

### 4) Fluxo de visão para imagem

Quando uma imagem é anexada:

- a imagem é convertida em base64;
- a app envia a imagem e a pergunta para o modelo de visão;
- o modelo analisa visualmente o conteúdo;
- retorna um texto descrevendo ou transcrevendo a informação visual;
- essa resposta pode ser exibida diretamente ao usuário.

### 5) Fluxo de OCR para PDF digitalizado

Quando um PDF não possui texto pesquisável:

- o app abre cada página com `PyMuPDF`;
- converte cada página para imagem;
- transforma a imagem em base64;
- chama o modelo de visão para fazer OCR da página;
- junta o texto extraído de todas as páginas;
- esse texto vira conteúdo textual do documento;
- a partir daí, ele entra no mesmo fluxo de RAG.

Esse é o caminho usado para documentos escaneados, como um CV digitalizado.

## Stack tecnológica

- Streamlit: interface web
- Python-dotenv: carregamento das variáveis de ambiente
- LangChain: orquestração do LLM e mensagens
- Groq: acesso ao LLM e ao modelo de visão
- DuckDuckGo Search: busca na web
- PyMuPDF (`fitz`): leitura/extracao de PDF
- FAISS: banco vetorial local
- LangChain Text Splitter: chunking de documentos
- Hugging Face Embeddings: modelagem semântica de textos
- Sentence Transformers: suporte ao pipeline de embeddings

## Estrutura do repositório

```text
Terminal-Bot/
├── app.py
├── requirements.txt
├── teste.py
├── README.md
├── .env
├── .gitignore
├── __pycache__/
└── venv/
```

## Requisitos

- Python 3.10+
- Chave API da Groq
- Acesso à internet para baixar modelos e fazer busca web

## Instalação

1. Entre na pasta do projeto:

```bash
cd /caminho/para/Terminal-Bot
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com a chave da API:

```env
GROQ_API_KEY=sua_chave_aqui
```

## Execução

### Iniciar a aplicação web

```bash
streamlit run app.py
```

Se a porta 8501 estiver ocupada, use outra porta:

```bash
streamlit run app.py --server.port 8502
```

## Variáveis importantes

- `GROQ_API_KEY`: chave de acesso à API da Groq
- `temperatura`: controla a criatividade da resposta do LLM
- `pesquisa_web`: habilita busca na internet
- `vector_db`: banco vetorial do documento anexado

## Troubleshooting

### Erro de chave da API

Mensagem comum:

- `GROQ_API_KEY não encontrada`

Solução:

- verificar se o arquivo `.env` existe;
- confirmar que a chave foi digitada corretamente;
- reiniciar a aplicação.

### Erro de importação de pacote

Se aparecer algo como:

- `Could not import ddgs python package`

Solução:

```bash
pip install -U ddgs
```

### Problema de porta

Se a porta 8501 estiver em uso:

```bash
streamlit run app.py --server.port 8502
```

## Observação importante

O README antigo falava de uma interface de terminal que não existe no estado atual do repositório. A implementação real do projeto está centralizada na interface web do Streamlit, e o fluxo principal de IA é baseado em:

- LLM para respostas conversacionais;
- visão para imagens e OCR;
- embeddings/RAG para documentos locais;
- busca web para contexto externo.

## Objetivo do projeto

O projeto foi construído como um protótipo de chatbot multimodal para:

- responder a perguntas gerais;
- trabalhar com documentos locais;
- interpretar imagens;
- processar PDFs digitalizados;
- buscar informação atual na web.

Este é um projeto funcional como demonstração de integração de IA com LangChain, Groq, Streamlit e recuperação de contexto.

---

Desenvolvido para explorar IA multimodal, RAG e assistentes conversacionais em Python.
