# 📧 Email Classifier - Classificação Inteligente de Emails

Uma aplicação web moderna que utiliza Inteligência Artificial para classificar emails e gerar respostas automáticas de forma profissional e eficiente.

## 🎯 Sobre o Projeto

O Email Classifier analisa o conteúdo de emails e determina se são:
- **Produtivo**: emails que exigem ação ou resposta (suporte, dúvidas, solicitações)
- **Improdutivo**: emails informativos ou sociais (agradecimentos, felicitações)

Além da classificação, a aplicação gera automaticamente uma resposta adequada ao contexto do email.

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.10+**
- **FastAPI** - Framework web moderno e de alto desempenho
- **Uvicorn** - Servidor ASGI
- **NLTK** - Processamento de Linguagem Natural
- **OpenAI API** - Inteligência Artificial para classificação e geração de respostas
- **PyPDF2** - Leitura de arquivos PDF
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5**
- **CSS3** - Design moderno e responsivo
- **JavaScript** - Vanilla JS, sem frameworks

## 📁 Estrutura do Projeto

```
Desafio AutoU/
├── backend/
│   ├── app.py                      # Aplicação FastAPI principal
│   ├── services/
│   │   ├── classifier.py           # Lógica de classificação
│   │   └── ai_service.py           # Integração com OpenAI
│   ├── utils/
│   │   └── text_preprocess.py      # Pré-processamento NLP
│   ├── requirements.txt            # Dependências Python
│   └── .env.example                # Exemplo de variáveis de ambiente
│
├── frontend/
│   ├── index.html                  # Interface principal
│   ├── style.css                   # Estilos
│   └── script.js                   # Lógica do cliente
│
├── README.md
└── .gitignore
```

## 🏗️ Arquitetura da Solução

### Fluxo de Processamento

1. **Entrada**: Usuário fornece email (texto ou arquivo .txt/.pdf)
2. **Pré-processamento**: 
   - Normalização (lowercase)
   - Remoção de pontuação e caracteres especiais
   - Tokenização
   - Remoção de stopwords (português e inglês)
3. **Classificação**: API OpenAI analisa o conteúdo
4. **Resposta**: Geração automática de resposta adequada
5. **Saída**: Exibição da categoria e resposta sugerida

### Componentes Principais

- **app.py**: API REST com endpoint `/classify`
- **classifier.py**: Orquestra a classificação e geração de resposta
- **ai_service.py**: Gerencia comunicação com OpenAI
- **text_preprocess.py**: Pipeline de processamento de texto
- **Frontend**: Interface amigável e responsiva

## 🔧 Como Rodar Localmente

### Pré-requisitos

- Python 3.10 ou superior
- Conta OpenAI com API Key ([obtenha aqui](https://platform.openai.com/api-keys))

### Passo 1: Clone o Repositório

```bash
git clone <seu-repositorio>
cd "Desafio AutoU"
```

### Passo 2: Configure o Backend

```bash
# Entre na pasta do backend
cd backend

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
# Copie o arquivo .env.example para .env
copy .env.example .env

# Edite o arquivo .env e adicione sua chave da OpenAI:
# OPENAI_API_KEY=sua_chave_aqui
```

### Passo 3: Inicie o Backend

```bash
# Ainda na pasta backend
python app.py
```

O backend estará rodando em: `http://localhost:8000`

### Passo 4: Abra o Frontend

```bash
# Em outro terminal, na pasta do projeto
cd frontend

# Abra o arquivo index.html no navegador
# Ou use um servidor HTTP simples:
python -m http.server 8080
```

Acesse: `http://localhost:8080`

## 📝 Como Usar

1. **Acesse a aplicação** no navegador
2. **Cole o texto do email** no campo de texto OU **faça upload** de um arquivo (.txt ou .pdf)
3. **Clique em "Classificar Email"**
4. **Veja o resultado**:
   - Categoria (Produtivo ou Improdutivo)
   - Resposta automática sugerida
5. **Clique em "Nova Classificação"** para analisar outro email

## 🧪 Exemplo de Uso

### Email Produtivo
**Entrada:**
```
Olá,

Estou tendo problemas ao acessar o sistema. Poderia me ajudar?

Obrigado
```

**Saída:**
- **Categoria**: Produtivo
- **Resposta**: "Olá! Recebi sua solicitação sobre o problema de acesso ao sistema. Vou verificar e retornar em breve com uma solução. Obrigado por entrar em contato."

### Email Improdutivo
**Entrada:**
```
Parabéns pelo excelente trabalho na apresentação de ontem!

Até logo.
```

**Saída:**
- **Categoria**: Improdutivo
- **Resposta**: "Muito obrigado pelo feedback positivo! Fico feliz que tenha gostado da apresentação."

## 🚀 Deploy

### Opção 1: Render

1. Crie conta no [Render](https://render.com)
2. Crie um novo Web Service
3. Conecte seu repositório GitHub
4. Configure:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python app.py`
   - **Environment Variables**: Adicione `OPENAI_API_KEY`
5. Deploy!

### Opção 2: Railway

1. Crie conta no [Railway](https://railway.app)
2. Crie novo projeto do GitHub
3. Configure variáveis de ambiente
4. Deploy automático

### Frontend Deploy

O frontend pode ser hospedado em:
- **Vercel** (recomendado)
- **Netlify**
- **GitHub Pages**

Lembre-se de atualizar a URL da API em `frontend/script.js`:
```javascript
const API_URL = 'https://sua-api-render.onrender.com';
```

## 🔒 Segurança

- ⚠️ **NUNCA** commite o arquivo `.env` com sua API Key
- Use variáveis de ambiente em produção
- O arquivo `.gitignore` já está configurado para proteger informações sensíveis

## 🛠️ Melhorias Futuras

- [ ] Autenticação de usuários
- [ ] Histórico de classificações
- [ ] Múltiplos modelos de IA
- [ ] Categorias personalizáveis
- [ ] Editor de respostas sugeridas
- [ ] Estatísticas e analytics
- [ ] API de webhooks

## 📄 Licença

Este projeto foi desenvolvido como parte de um desafio técnico.

## 👤 Autor

Desenvolvido com ❤️ seguindo as melhores práticas de Clean Code e Engenharia de Software.

---

**🌟 Se este projeto foi útil, considere dar uma estrela no repositório!**
