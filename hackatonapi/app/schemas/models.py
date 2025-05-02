from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    """
    Modelo para la solicitud de prompt de texto.
    
    Attributes:
        prompt (str): Texto de entrada del usuario
    """
    prompt: str

class TextResponse(BaseModel):
    """
    Modelo para la respuesta de texto.
    
    Attributes:
        text (str): Texto de respuesta generado
    """
    text: str

class QuestionRequest(BaseModel):
    """
    Modelo para la solicitud de pregunta a la IA.
    
    Attributes:
        text (str): Contexto o texto de referencia
        question (str): Pregunta específica del usuario
    """
    text: str
    question: str

class AnswerResponse(BaseModel):
    """
    Modelo para la respuesta de la IA.
    
    Attributes:
        data (str): Respuesta generada por la IA
        confidence (Optional[float]): Podrías añadir esto en el futuro
    """
    data: str
    # confidence: Optional[float] = None  # Ejemplo de campo opcional para futuro uso