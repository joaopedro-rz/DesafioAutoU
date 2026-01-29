# Desafio AutoU - Classificador de E-mail

Aplicação web para classificar e-mails (Produtivo/Improdutivo) e sugerir uma resposta automática.

## Deploy (Render)

O aplicativo está em deploy na plataforma Render:

- Site estático (aplicação completa): https://desafioautou-w20m.onrender.com
- Web Service (backend/API): https://desafioautou-c87f.onrender.com

## Como executar localmente

### Pré-requisitos

- Windows
- Python 3.10 (recomendado; é o que o deploy usa)
- Token da Hugging Face com permissão de **Inference Providers** (variável `HF_TOKEN`)

### 1) Backend (API)

No PowerShell:

```bash
cd backend

# criar venv
py -3.10 -m venv venv

# ativar
venv\Scripts\Activate.ps1

# instalar dependências
python -m pip install -U pip
pip install -r requirements.txt

# iniciar API
python app.py
```

API em `http://127.0.0.1:8000`.

### 2) Frontend

Em outro terminal:

```bash
cd frontend
python -m http.server 8080
```

Acesse `http://127.0.0.1:8080`.

## Configuração da IA (Hugging Face)

Crie/edite `backend/.env` com o mínimo:

```env
AI_PROVIDER=huggingface
HF_TOKEN=hf_...

# opcional (se quiser trocar o modelo)
HUGGINGFACE_MODEL=meta-llama/Llama-3.2-1B-Instruct
# opcional (normalmente não precisa mudar)
HUGGINGFACE_ROUTER_BASE_URL=https://router.huggingface.co/v1
```

Dica: escolha um modelo que apareça em `https://router.huggingface.co/v1/models`.

## Problemas comuns

- Se der erro ao instalar dependências (ex.: `pydantic_core`), confirme que o venv foi criado com `py -3.10`.
- Se a IA responder com erro de permissão, confira se seu token tem acesso a **Make calls to Inference Providers**.
