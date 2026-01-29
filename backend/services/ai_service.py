import os
from dotenv import load_dotenv
from pathlib import Path

_backend_dir = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=_backend_dir / ".env")


class AIService:
    """Serviço de integração com IA (Hugging Face ou OpenAI)"""
    
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "huggingface").lower()

        if self.provider == "huggingface":
            self.api_key = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
            # Docs: https://huggingface.co/docs/inference-providers/index
            self.hf_router_base_url = os.getenv(
                "HUGGINGFACE_ROUTER_BASE_URL",
                "https://router.huggingface.co/v1",
            )
            self.model = os.getenv(
                "HUGGINGFACE_MODEL",
                "meta-llama/Llama-3.2-1B-Instruct",
            )
            if not self.api_key:
                raise ValueError(
                    "Token do Hugging Face não encontrado. Configure HF_TOKEN (recomendado) "
                    "ou HUGGINGFACE_API_KEY no arquivo .env"
                )
        else:
            # OpenAI
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY não encontrada. Configure no arquivo .env")
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            self._client = None
    
    @property
    def client(self):
        """Lazy initialization do cliente OpenAI"""
        if self.provider == "openai":
            if self._client is None:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    timeout=30.0,
                    max_retries=2
                )
            return self._client
        return None
    
    def classify_email(self, prompt: str) -> str:
        """
        Envia prompt para a IA e retorna a resposta
        
        Args:
            prompt: Prompt com instruções de classificação
        
        Returns:
            Resposta da IA com categoria e resposta sugerida
        """
        try:
            if self.provider == "huggingface":
                return self._generate_with_huggingface(prompt)
            else:
                return self._classify_with_openai(prompt)
        except Exception as e:
            raise Exception(f"Erro ao comunicar com IA: {str(e)}")
    
    def _generate_with_huggingface(self, prompt: str) -> str:
        """Gera texto usando Hugging Face via endpoint OpenAI-compatível do router."""
        from openai import OpenAI

        client = OpenAI(
            base_url=self.hf_router_base_url,
            api_key=self.api_key,
            timeout=60.0,
            max_retries=1,
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Responda SEMPRE com EXATAMENTE 2 linhas, sem Markdown e sem texto extra. "
                        "Linha 1: 'CATEGORIA: PRODUTIVO' ou 'CATEGORIA: IMPRODUTIVO'. "
                        "Linha 2: 'RESPOSTA: <resposta curta e profissional>'."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=float(os.getenv("HUGGINGFACE_TEMPERATURE", "0.2")),
            max_tokens=int(
                os.getenv(
                    "HUGGINGFACE_MAX_TOKENS",
                    os.getenv("HUGGINGFACE_MAX_NEW_TOKENS", "300"),
                )
            ),
        )

        return response.choices[0].message.content.strip()

    def _classify_with_openai(self, prompt: str) -> str:
        """Classifica usando OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Responda SEMPRE com EXATAMENTE 2 linhas, sem Markdown e sem texto extra. "
                        "Linha 1: 'CATEGORIA: PRODUTIVO' ou 'CATEGORIA: IMPRODUTIVO'. "
                        "Linha 2: 'RESPOSTA: <resposta curta e profissional>'."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
