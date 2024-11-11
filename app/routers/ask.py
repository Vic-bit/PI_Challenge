from fastapi import APIRouter
from pydantic import BaseModel
from app.dependencies import cohere_client, collection
from langdetect import detect

# Intanciar router
router = APIRouter()

# Definir el modelo de request
class QuestionRequest(BaseModel):
    user_name: str
    question: str

# Crear el endpoint para recibir preguntas
@router.post("/ask")
async def ask_question(request: QuestionRequest):

    # Obtener embeddings de la pregunta
    question_embedding = cohere_client.embed(model="large", 
                                    texts=[request.question]).embeddings[0]
    
    # Consultar el contenido en ChromaDB
    results = collection.query(query_embeddings=[question_embedding], 
                               n_results=1)
    
    # Extraer el documento más relevante como contexto
    context = results['documents'][0]  

    # Detectar el idioma de la pregunta
    detected_language = detect(request.question)

    # Detectar idioma para responder en el mismo idioma
    if detected_language == 'en':
        language_response = "Answer in English, in the third person, in a single clear and concise sentence, and include emojis at the end to summarize the content of the response."
    elif detected_language == 'pt':
        language_response = "Responda em português, na terceira pessoa numa única frase clara e concisa, e inclua emojis no final para resumir o conteúdo da resposta."
    else:
        language_response = "Responde en español, en tercera persona, en una sola oración clara y concisa, e incluye emojis al final para resumir el contenido de la respuesta."

    print("Lenguaje detectado", detected_language)

    # Crear el prompt para Cohere con las instrucciones que necesitas
    prompt = (f"{language_response}\n\nContexto: {context}\nPregunta: {request.question}\nRespuesta:")

        # Generar la respuesta usando el contexto recuperado
    response = cohere_client.generate(
        prompt= prompt, 
        max_tokens=50,
        model="command",
        temperature=0.0,
    )

    answer = response.generations[0].text.strip()

    return {"answer": answer, "context": context}
