from fastapi import APIRouter, status
from app.schemas.models import PromptRequest, QuestionRequest, TextResponse, AnswerResponse
from app.services.text_service import get_text_prompt, get_response_ia

router = APIRouter(
    prefix="/api/v1",
    tags=["Servicios de Texto e IA"]
)

@router.post(
    "/gettextprompt",
    response_model=TextResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener texto de respuesta para un prompt",
    description="Genera una respuesta estándar basada en el prompt de entrada"
)
async def gettextprompt_endpoint(request: PromptRequest):
    """
    Endpoint para obtener una respuesta de texto basada en un prompt.
    
    - **prompt**: Texto de entrada del usuario
    """
    return get_text_prompt(request)

@router.post(
    "/getresponseia",
    response_model=AnswerResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener respuesta de IA",
    description="Genera una respuesta simulando inteligencia artificial"
)
async def getresponseia_endpoint(request: QuestionRequest):
    """
    Endpoint para obtener una respuesta simulando IA.
    
    - **text**: Contexto o texto de referencia
    - **question**: Pregunta específica del usuario
    """
    return get_response_ia(request)