import re


# Lista de stopwords em português e inglês
STOPWORDS = {
    # Português
    'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 
    'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'ao', 
    'ele', 'das', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 
    'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 
    'mesmo', 'aos', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'você', 'essa', 
    'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas', 'qual', 
    'nós', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'dele', 'tu', 'te', 
    'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 
    'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 
    'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'ser', 'foi', 'ter', 'sido',
    # Inglês
    'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'as', 'it', 
    'that', 'by', 'at', 'from', 'this', 'be', 'are', 'or', 'an', 'was', 'but', 
    'not', 'have', 'has', 'had', 'we', 'you', 'they', 'will', 'can', 'if', 'their', 
    'which', 'about', 'all', 'were', 'when', 'there', 'been', 'who', 'would', 'what', 
    'so', 'up', 'out', 'them', 'than', 'she', 'him', 'her', 'could', 'been', 'should'
}


def preprocess_text(text: str) -> str:
    """
    Pré-processa o texto do email
    
    Etapas:
    1. Normalização para lowercase
    2. Remoção de caracteres especiais e pontuação
    3. Tokenização simples
    4. Remoção de stopwords
    5. Reconstrução do texto
    
    Args:
        text: Texto original do email
    
    Returns:
        Texto pré-processado
    """

    # Normalizar para lowercase
    text = text.lower()
    
    # Remover URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remover emails
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remover pontuação e caracteres especiais
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remover números
    text = re.sub(r'\d+', '', text)
    
    # Remover espaços múltiplos
    text = re.sub(r'\s+', ' ', text)
    
    # Tokenização simples (split por espaços)
    tokens = text.split()
    
    # Remover stopwords e palavras muito curtas
    filtered_tokens = [
        word for word in tokens 
        if word not in STOPWORDS and len(word) > 2
    ]
    
    # Reconstruir texto
    processed_text = ' '.join(filtered_tokens)
    
    return processed_text.strip()
