
# Abre el archivo .docx y lo devuelve como texto
def open_content(path):
    # Abrir el archivo .docx
    doc = Document(path)
    
    # Extraer todo el texto del documento
    content = ''
    for para in doc.paragraphs:
        content += para.text + '\n'  # Concatenar cada párrafo con salto de línea
    
    return content
