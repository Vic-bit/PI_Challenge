from fastapi import APIRouter
from pydantic import BaseModel
from app.dependencies import cohere_client, collection

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

    # Crear el prompt para Cohere con las instrucciones que necesitas
    prompt = f"Contexto: {context}\nPregunta: {request.question}\nRespuesta:"

    # Generar la respuesta usando el contexto recuperado
    response = cohere_client.generate(
        prompt= prompt, 
        max_tokens=50,
        model="command",
        temperature=0.1,
    )

    answer = response.generations[0].text.strip()

    return {"answer": answer, "context": context}
