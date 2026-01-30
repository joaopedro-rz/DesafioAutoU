from services.ai_service import AIService


class EmailClassifier:
    """Classificador de emails usando IA"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.categories = {
            "produtivo": "Produtivo",
            "improdutivo": "Improdutivo"
        }
    
    def classify_and_respond(self, original_text: str, processed_text: str) -> dict:
        # Criar prompt para a IA
        prompt = self._create_classification_prompt(original_text)
        
        # Obter classificação e resposta da IA
        ai_response = self.ai_service.classify_email(prompt)
        
        # Extrai categoria e resposta
        category = self._extract_category(ai_response)
        response = self._extract_response(ai_response)
        
        return {
            "category": category,
            "response": response
        }
    
    def _create_classification_prompt(self, email_text: str) -> str:
        # Cria o prompt para a IA
        return f"""Analise o seguinte email e realize duas tarefas:

1. CLASSIFICAÇÃO: Determine se o email é:
   - PRODUTIVO: requer ação, resposta, ou trata de assuntos de trabalho/suporte/dúvidas/solicitações
   - IMPRODUTIVO: é apenas informativo, social, agradecimento, felicitação, spam

2. RESPOSTA: Gere uma resposta curta, educada e profissional adequada ao contexto.

Email:
{email_text}

Regras obrigatórias de resposta:
- Responda com EXATAMENTE 2 linhas.
- Não use Markdown, listas, títulos, aspas, nem texto extra.
- A primeira linha deve começar com "CATEGORIA:".
- A segunda linha deve começar com "RESPOSTA:".

Formato obrigatório (copie o formato, substituindo apenas os valores):
CATEGORIA: PRODUTIVO
RESPOSTA: (sua resposta sugerida)"""
    
    def _extract_category(self, ai_response: str) -> str:
        """Extrai a categoria da resposta da IA"""
        lines = ai_response.split('\n')
        for line in lines:
            if 'CATEGORIA:' in line.upper():
                category = line.split(':', 1)[1].strip().upper()
                if 'PRODUTIVO' in category and 'IMPRODUTIVO' not in category:
                    return "Produtivo"
                elif 'IMPRODUTIVO' in category:
                    return "Improdutivo"
        
        # Fallback: análise do conteúdo
        if 'IMPRODUTIVO' in ai_response.upper():
            return "Improdutivo"
        return "Produtivo"
    
    def _extract_response(self, ai_response: str) -> str:
        """Extrai a resposta sugerida da resposta da IA"""
        lines = ai_response.split('\n')
        response_started = False
        response_parts = []
        
        for line in lines:
            if 'RESPOSTA:' in line.upper():
                response_started = True
                # Pega o que vem depois de "RESPOSTA:"
                response_parts.append(line.split(':', 1)[1].strip())
            elif response_started and line.strip():
                response_parts.append(line.strip())
        
        response = ' '.join(response_parts)
        
        if not response:
            response = "Obrigado pelo seu email. Entraremos em contato em breve."
        
        return response
