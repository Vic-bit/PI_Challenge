# PI_Challenge

## Descipción

Este proyecto es una API de preguntas y respuestas basada en FastAPI, diseñada para responder a consultas en el mismo idioma en el que se realizan. La aplicación utiliza embeddings de Cohere para analizar las preguntas, ChromaDB para buscar contexto relevante en una base de datos de vectores, y ofrece respuestas concisas y en tercera persona. El proyecto admite múltiples idiomas (español, inglés y portugués) y emplea una arquitectura modular y escalable.

![image](https://github.com/user-attachments/assets/ea1ab16d-a905-49a5-8666-fe70e53e054e)

## Características

- **Multi-idioma**: La API detecta el idioma de la pregunta y responde en el mismo idioma (español, inglés o portugués).
- **Integración con Cohere y ChromaDB**: Utiliza Cohere para generar embeddings y ChromaDB para consultar el contexto más relevante.
- **Respuesta concisa y resumida**: Las respuestas son concisas, en tercera persona y acompañadas de emojis que resumen el contenido.
- **Configuración de dependencias**: Se proporciona un archivo `requirements.txt` con todas las dependencias necesarias.

## Estructura del Proyecto

```python
PI_Challenge
├── /app
│   ├── /routers
│   │   ├──__init__.py      # Archivo recomendado en la documentación
│   │   └── ask.py          # Se definen las rutas de las preguntas
│   ├── main.py             # Se inicializa FastAPI y se incluyen los routers
│   └── dependencies.py     # Se inicaliza Cohere y Chroma además de tener funciones útiles
├── /static   
│   └── /documento.docx     # Documento a usar por el RAG        
├── requirements.txt        # Dependencias necesarias
└── README.md               # Documentación del proyecto
```

## Instalación

El proyecto fue desarrollado en python, requiere python>=3.8.

1. Para clonar el repositorio localmente, dirigirse al directorio deseado y ejecutar:

```python
git clone https://github.com/Vic-bit/PI_Challenge.git
cd PI_Challenge
```

2. Se recomienda crear un entorno virtual para evitar conflictos con otras instalaciones en el sistema. Tenga en cuenta de que debe crear fuera de la carpeta del proyecto el entorno virtual o incluirlo en .gitignore.

- Crear entorno vitual para Windows:

```python
python -m venv pienv
```

- Crear entorno global para macOS o Linux:

```python
python3 -m venv pienv
```

3. Activar el entorno virtual 

- En Windows:

```python
pienv\Scripts\activate
```

- En macOS y Linux:

```python
source pienv/bin/activate
```

4. Instalar las dependencias desde requirements.txt:

```python
pip install -r requirements.txt
```

5. Por razones de seguridad la API key de Cohere se agregó a .gitignore. Se recomienda crear una API key de Cohere desde su página web

- Debe registrarse:
https://dashboard.cohere.com/welcome/login 

- Dirgierse a la sección de API Keys donde econtrará las Trial keys de las cuales ya tiene por default su key, la cual puede copiar.
https://dashboard.cohere.com/api-keys

- Crear en el proyecto un archivo .env en la carpeta raíz y crear una variable, copiar la api key y pegarla para asignar a la variable cohere_api_key sin las comillas:

```python
cohere_api_key = "ingrese aquí su api key de cohere"
```

## Uso 
Una vez realizada la instalación solo resta ejecutar la aplicación y realizar consultas.

1. Desde la terminal ejecutar el siguiente comando bash:

```python
uvicorn app.main:app --reload
```

Esto iniciará el servidor en http://127.0.0.1:8000.

2. Ingresar al localhost desde su browser:

```python
http://127.0.0.1:8000/docs
```

3. Para realizar una pregunta, envía una solicitud POST al endpoint /ask con el siguiente formato:

```python
{
  "user_name": "NombreUsuario",
  "question": "Tu pregunta aquí"
}
```

La API devolverá una respuesta en el mismo idioma, en una oración clara y concisa con emojis de resumen.


## Ejemplos

#### Pregunta en español
Pregunta: "¿Quién es Zara?"
Respuesta: "Zara es un intrépido explorador del universo de Zenthoria, que viaja de planeta a planeta en busca de la paz. 🪐 \n\n¿Cómo le va en"


#### Pregunta en inglés
Question: "Who is Zara?"
Answer: "Zara is an intrepid explorer in the distant galactic galaxy of Zenthoria, who discovers an ancient artifact that may hold the key to peace between two alien civilizations on the brink of intergalactic war. ⭐️🪐�"


#### Pregunta en portugués
Pergunta: "Quem é a Zara?"
Resposta: "Zara é um intrépido explorador de la distante galaxia de Zenthoria. 🌌🏃‍♀️ É a arqueólogo que descobre um antigo artefacto que"


## Conclución

Se implementó un sistema RAG que permite a los usuarios obtener respuestas basadas en un documento cargado. Se utilizó Cohere para generar embeddings y ChromaDB para buscar información relevante, todo accesible a través de una API de FastAPI.


