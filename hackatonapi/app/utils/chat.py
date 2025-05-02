from langchain_ibm.chat_models import ChatWatsonx
from docling.document_converter import DocumentConverter
import os
from dotenv import load_dotenv
#Configurara memoria
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
#Configurara embedded  model
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer
#In Memory Vector Store
from langchain_core.vectorstores import InMemoryVectorStore
#Consumo core
from repository.core import search_file_content as filename_search
#Dividir el documento en chunks
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
#Convertr archivos
import markdown
from bs4 import BeautifulSoup

load_dotenv()

MODEL_ID=os.getenv('MODEL_ID')
URL=os.getenv('URL')
API_KEY=os.getenv('API_KEY')
PROJECT_ID=os.getenv('PROJECT_ID')

CONNECTION_STRING=os.getenv('CONNECTION_STRING')
COLLECTION=os.getenv('COLLECTION')

#Modelo de embeddings
embeddings_model_path = "ibm-granite/granite-embedding-107m-multilingual"
embeddings_model = HuggingFaceEmbeddings(
    model_name=embeddings_model_path,
)
embeddings_tokenizer = AutoTokenizer.from_pretrained(embeddings_model_path)
#In Memory Vector Store
vector_store = InMemoryVectorStore(embeddings_model)

#Initialize Granite model with watsonx
llm = ChatWatsonx(
    model_id=MODEL_ID,
    url=URL,
    apikey=API_KEY,
    project_id=PROJECT_ID,
)

def recuperar_documento(doc_name):
    try:
        #Traer el documento
        filename = filename_search(doc_name)
        #Transformar
        html = markdown.markdown(filename)
        plain_text = BeautifulSoup(html, "html.parser").get_text()
        return plain_text
    except Exception as e:
        print(f"Error al recuperar el documento: {e}")
        return None

def transformar_documento(plain_text):
    #Dividir el documento en chunks
    documents = Document(page_content=plain_text)
    try:
        text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=embeddings_tokenizer,
            chunk_size=embeddings_tokenizer.max_len_single_sentence,
            chunk_overlap=0,
        )
        texts = text_splitter.split_documents([documents])
        doc_id = 0
        for text in texts:
            text.metadata["doc_id"] = (doc_id:=doc_id+1)
        print(f"{len(texts)} text document chunks created")
        return texts
    except Exception as e:
        print(f"Error al dividir el documento: {e}")
        return None

@staticmethod
def chat_with_user(doc_name):
    #Pedir el docuemento
    documento = recuperar_documento(doc_name)
    #Procesar el documento
    texts = transformar_documento(documento)
    #Guardar enbeddings en memoria
    ids = vector_store.add_documents(texts)    
    #Crear un retriever para buscar en el vector store
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    #Configuarar memoria para mantener el contexto de la conversacion
    memory = ConversationBufferMemory(
        return_messages=True,
    )
    # Definir el prompt con historial incluido
    prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente útil de IBM Watsonx Granite."
     "Tu objetivo principal es proporcionar la información mínima necesaria para responder la pregunta del usuario de forma precisa y concisa, utilizando únicamente el contexto disponible."
     "Todas tus respuestas deben ser estrictamente en español. No utilices ninguna palabra o frase en inglés."
     "Si la información proporcionada no es suficiente para ofrecer una respuesta útil, indica 'No tengo información suficiente para responder esa pregunta'."
     "Evita cualquier explicación adicional o información superflua. Sé directo y enfócate en responder la pregunta central."
     ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    ])

    question = doc_name
        #if question.lower() in ["salir", "exit", "quit"]:
            #break

    #Recuperar documentos relevantes
    relevant_docs = retriever.invoke(question)
    #Concatenar los documentos relevantes
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    # Preparar el prompt con historial y entrada actual
    messages = prompt.invoke({
        "input": f"{context}\n\nPregunta del usuario: {question}",
        "history": memory.chat_memory.messages
    })

    # Llamar al modelo con el prompt ya procesado
    response = llm.invoke(messages)

    # Guardar mensajes en memoria
    memory.chat_memory.add_user_message(question)
    memory.chat_memory.add_ai_message(response.content)

    # Mostrar respuesta
    print("Bot:", response.content)
    return response.content



