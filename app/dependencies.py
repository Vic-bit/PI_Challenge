from dotenv import load_dotenv
import uuid
import os 
import cohere
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document

# Función para configurar las api keys
def configure():
    load_dotenv()

# Define la función de embeddings utilizando Cohere
def get_embeddings(text):
    # Almacena la respuesta de la API de Cohere, que contiene con los embeddings
    response = cohere_client.embed(model="large", 
                                   texts=[text])

    # Devuelve el primer embedding de la respuesta, como una lista de floats
    return response.embeddings[0]

# Abre el archivo .docx y lo devuelve como texto
def open_content(path):
    # Abrir el archivo .docx
    doc = Document(path)
    
    # Extraer todo el texto del documento
    content = ''
    for para in doc.paragraphs:
        content += para.text + '\n'  # Concatenar cada párrafo con salto de línea
    
    return content

# Divide en fragmentos a content y lo agrega a collection
def process_and_add_to_db(content, collection):
    # Instanciar RecursiveCharacterTextSplitter para agregar contenido a Chroma
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], 
        chunk_size=200, 
        chunk_overlap=30
    )

    # Dividir el content en fragmentos
    docs = text_splitter.create_documents([content])

    for doc in docs:
        # Generar identificador único 
        uuid_name = str(uuid.uuid1())

        # Almacena la respuesta de la API de Cohere, con los embeddings
        # Devuelve el primer embedding de la respuesta, como una lista de floats
        doc_embedding = cohere_client.embed(model="large", 
                                    texts=[doc.page_content]).embeddings[0]

        # Añadir cada fragmento a la colección en Chroma
        collection.add(ids=[uuid_name],                 
                        documents=[doc.page_content], 
                        embeddings=[doc_embedding])


# Configurar la api key
configure()

# Configurar clave de API de Cohere
COHERE_API_KEY = os.getenv("cohere_api_key")

# Instanciar cliente de Cohere
cohere_client = cohere.Client(COHERE_API_KEY)

# Instanciar cliente de Chroma
chroma_client = chromadb.Client()

# Crear una función de embeddings que utiliza Cohere
cohere_ef = embedding_functions.CohereEmbeddingFunction(api_key=COHERE_API_KEY, 
                                                        model_name="large")

# Definir opciones de metadatos para Chroma, con la métrica de similitud
metadata_options = {"hnsw:space": "ip"}

# Collección en Chroma
collection = chroma_client.get_or_create_collection(
    name="my_collection",           # Nombre de la colección
    metadata=metadata_options,      # Asigna los metadatos a la colección
    embedding_function=cohere_ef    # Define la función de embeddings a usar
)

# Leer y procesar el contenido para añadirlo a la colección en Chroma
content = open_content('static/documento.docx')
process_and_add_to_db(content, collection)  # Llama a la función solo una vez