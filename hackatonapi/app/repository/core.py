from langchain_ibm.chat_models import ChatWatsonx
from pydantic import BaseModel, Field
from pymongo import MongoClient
from docling.document_converter import DocumentConverter
import gridfs
import pymupdf4llm
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_ID=os.getenv('MODEL_ID')
URL=os.getenv('URL')
API_KEY=os.getenv('API_KEY')
PROJECT_ID=os.getenv('PROJECT_ID')

CONNECTION_STRING=os.getenv('CONNECTION_STRING')
COLLECTION=os.getenv('COLLECTION')


#Initialize Granite model with watsonx
llm = ChatWatsonx(
    model_id=MODEL_ID,
    url=URL,
    apikey=API_KEY,
    project_id=PROJECT_ID,
)

@staticmethod
def search_file_content(prompt):

    #JSON structure that will return the file name information
    class File(BaseModel):
        file_name: str = Field(description="The name of the file or document mentioned in the user's question")

    #Structured model
    structured_llm = llm.with_structured_output(File.model_json_schema())

    #Result
    file = structured_llm.invoke(prompt)
    file_name=file['file_name']

    print(f'resultad: {file}')
    file_content=search_file(file_name)

    return file_content

def search_file(filename):
    #Connecting to the document repository
    client = MongoClient(CONNECTION_STRING)
    #Collection
    db = client[COLLECTION]
    idDocument = ''
    extracted = ''
    collectionGlobal = ''
    #Browse file list
    for collection in db.list_collection_names():
        try:
            #Check if the file name exists
            if (collection.__contains__(filename)):
                if (collection.__contains__('.file')):
                    collectionGlobal=collection
                    fs = gridfs.GridFS(db, collection=collection.replace('.files',''))
                    for document in fs.find():
                        idDocument = document._id
        except:
            #If file not found
            print('file not found')
            idDocument = ''
            collectionGlobal = ''

    #If file was found
    if (idDocument != '' and collectionGlobal != ''):
        cut = collectionGlobal.replace('.files', '')
        print(f'Filename: {idDocument}, Collection: {cut}')
        fs = gridfs.GridFSBucket(db, bucket_name=cut)

        #Download repository file
        iter = fs.open_download_stream(idDocument)
        content = iter.read()

        #Save file temporarily
        f = open(filename, 'x+b')
        f.write(content)

        #pymupdf4llm
        #Generate text in MarkDown format
        md_read = pymupdf4llm.LlamaMarkdownReader()
        data = md_read.load_data(filename)

        #docling
        #source = filename  # document per local path or URL
        #converter = DocumentConverter()
        #result = converter.convert(source)
        #extracted = result.document.export_to_markdown()

        #Concatenate markdown
        for page in data:
            extracted = extracted +page.to_dict()['text']

        f.close()
    
        #Delete temporary file
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                print('error eliminar')
    print(extracted)

    return extracted