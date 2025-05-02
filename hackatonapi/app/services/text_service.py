from app.schemas.models import PromptRequest, QuestionRequest, TextResponse, AnswerResponse
from app.utils.chat import chat_with_user

def get_text_prompt(payload: PromptRequest) -> TextResponse:
    """
    Genera una respuesta de texto estándar para problemas de impresora.
    
    Args:
        payload (PromptRequest): Contiene el prompt del usuario
        
    Returns:
        TextResponse: Respuesta estructurada con el texto de ayuda
    """
    result = chat_with_user(payload.prompt)
    return TextResponse(text=result)

def get_response_ia(payload: QuestionRequest) -> AnswerResponse:
    """
    Procesa la pregunta y genera una respuesta simulando IA.
    
    Args:
        payload (QuestionRequest): Contiene el texto y la pregunta
        
    Returns:
        AnswerResponse: Respuesta estructurada con la 'data' procesada
    """
    result = chat_with_user(payload.question)
    # Aquí podrías añadir lógica más compleja en el futuro
    return AnswerResponse(data=result)