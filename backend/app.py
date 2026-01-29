from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import PyPDF2
from io import BytesIO
from typing import Optional

from services.classifier import EmailClassifier
from utils.text_preprocess import preprocess_text

app = FastAPI(title="Email Classifier API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar o classificador
classifier = EmailClassifier()


@app.get("/")
async def root():
    """Endpoint de verificação de saúde da API"""
    return {"message": "Email Classifier API está online", "status": "active"}


@app.post("/classify")
async def classify_email(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Classifica um email e gera resposta automática
    
    Args:
        text: Texto do email (opcional)
        file: Arquivo .txt ou .pdf (opcional)
    
    Returns:
        Categoria do email e resposta sugerida
    """
    try:
        # Validar entrada
        if not text and not file:
            raise HTTPException(
                status_code=400,
                detail="É necessário fornecer texto ou arquivo"
            )
        
        email_content = ""
        
        # Processar arquivo se fornecido
        if file:
            content = await file.read()
            
            if file.filename.endswith('.txt'):
                email_content = content.decode('utf-8')
            
            elif file.filename.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(BytesIO(content))
                email_content = ""
                for page in pdf_reader.pages:
                    email_content += page.extract_text()
            
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Formato não suportado. Use .txt ou .pdf"
                )
        
        # Usar texto se fornecido
        if text:
            email_content = text
        
        # Validar conteúdo
        if not email_content.strip():
            raise HTTPException(
                status_code=400,
                detail="O conteúdo do email está vazio"
            )
        
        # Pré-processar texto
        processed_text = preprocess_text(email_content)
        
        # Classificar e gerar resposta
        result = classifier.classify_and_respond(email_content, processed_text)
        
        return JSONResponse(content={
            "success": True,
            "category": result["category"],
            "response": result["response"],
            "original_text": email_content[:200] + "..." if len(email_content) > 200 else email_content
        })
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar email: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
