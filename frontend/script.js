// Configuração da API
const API_URL = 'https://desafioautou-c87f.onrender.com';

// Elementos do DOM
const emailForm = document.getElementById('emailForm');
const emailText = document.getElementById('emailText');
const emailFile = document.getElementById('emailFile');
const fileLabel = document.getElementById('fileLabel');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const categoryResult = document.getElementById('categoryResult');
const responseResult = document.getElementById('responseResult');

// Atualizar label quando arquivo for selecionado
emailFile.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        // O HTML já possui um ícone no label; aqui atualizamos apenas o texto.
        fileLabel.textContent = file.name;
        // Limpar textarea se arquivo for selecionado
        emailText.value = '';
    }
});

// Limpar arquivo se texto for digitado
emailText.addEventListener('input', () => {
    if (emailText.value.trim()) {
        emailFile.value = '';
        fileLabel.textContent = 'Escolher arquivo (.txt ou .pdf)';
    }
});

// Submeter formulário
emailForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validar entrada
    const hasText = emailText.value.trim();
    const hasFile = emailFile.files.length > 0;
    
    if (!hasText && !hasFile) {
        showError('Por favor, insira um texto ou selecione um arquivo.');
        return;
    }
    
    // Preparar FormData
    const formData = new FormData();
    
    if (hasText) {
        formData.append('text', emailText.value);
    }
    
    if (hasFile) {
        formData.append('file', emailFile.files[0]);
    }
    
    // Mostrar loading
    setLoading(true);
    hideError();
    hideResult();
    
    try {
        // Fazer requisição
        const response = await fetch(`${API_URL}/classify`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Erro ao processar email');
        }
        
        if (data.success) {
            showResult(data.category, data.response);
        } else {
            throw new Error('Erro desconhecido ao processar email');
        }
        
    } catch (error) {
        showError(error.message || 'Erro ao conectar com o servidor. Verifique se o backend está rodando.');
    } finally {
        setLoading(false);
    }
});

// Funções auxiliares
function setLoading(loading) {
    if (loading) {
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
    } else {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function showResult(category, response) {
    categoryResult.textContent = category;
    categoryResult.className = `category-badge category-${category.toLowerCase()}`;
    responseResult.textContent = response;
    
    resultDiv.style.display = 'block';
    emailForm.style.display = 'none';
    
    // Scroll para o resultado
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResult() {
    resultDiv.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorDiv.style.display = 'flex';
    
    // Esconder erro após 5 segundos
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorDiv.style.display = 'none';
}

function resetForm() {
    emailForm.reset();
    emailText.value = '';
    emailFile.value = '';
    fileLabel.textContent = 'Escolher arquivo (.txt ou .pdf)';
    
    hideResult();
    hideError();
    emailForm.style.display = 'flex';
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Verificar status da API ao carregar
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_URL}/`);
        if (!response.ok) {
            console.warn('API pode não estar acessível');
        }
    } catch (error) {
        console.warn('Não foi possível conectar à API. Verifique se o backend está rodando.');
    }
});
