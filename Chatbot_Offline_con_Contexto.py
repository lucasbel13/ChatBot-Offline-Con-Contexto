import ollama  # Librería para interactuar con Ollama
import threading  # Para manejar tareas en paralelo (ej: mostrar animación de "Pensando...")
import time  # Para gestionar pausas en la animación
import mysql.connector as mysql  # Para conectar con la base de datos MySQL
import os
import PyPDF2  # Para leer archivos PDF
import docx  # Para leer documentos Word (.docx)
import pandas as pd  # Para leer archivos Excel

# =========================
# FUNCIONES PARA BASE DE DATOS
# =========================
def conectar_db():
    """
    Conecta a la base de datos MySQL usando utf8mb4 para soportar caracteres Unicode completos.
    Asegúrate de que la base de datos 'chatbot' y la tabla 'historial_chat' existen.
    """
    return mysql.connect(
        host="localhost",
        user="root",
        password="Contraseña",
        database="chatbot",
        auth_plugin="mysql_native_password",  # Usar mysql_native_password para evitar problemas de autenticación
        charset="utf8mb4"  # Especifica el charset para soportar emojis y otros caracteres Unicode
    )


def guardar_mensaje(usuario, mensaje):
    """
    Guarda un mensaje en la tabla 'historial_chat' de la base de datos.
    
    :param usuario: Identificador del emisor (ej. "Usuario" o "Mistral")
    :param mensaje: Contenido del mensaje
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO historial_chat (usuario, mensaje) VALUES (%s, %s)", (usuario, mensaje))
        conexion.commit()
    except mysql.Error as err:
        print(f"❌ Error al guardar el mensaje: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

def ver_historial():
    """
    Recupera y muestra los últimos 10 mensajes almacenados en el historial del chat.
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario, mensaje FROM historial_chat ORDER BY id DESC LIMIT 10;")
        historial = cursor.fetchall()
        
        print("\n📜 Historial de Chat:")
        for usuario, mensaje in historial:
            print(f"{usuario}: {mensaje}")
    except mysql.Error as err:
        print(f"❌ Error al recuperar historial: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

# =========================
# FUNCIONES PARA EXTRAER TEXTO DE DOCUMENTOS
# =========================
def extraer_texto_pdf(ruta):
    """
    Extrae y retorna el texto de un archivo PDF.
    """
    texto = ""
    try:
        with open(ruta, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            for pagina in lector.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        texto = f"Error al extraer PDF: {e}"
    return texto

def extraer_texto_docx(ruta):
    """
    Extrae y retorna el texto de un archivo Word (.docx).
    """
    texto = ""
    try:
        documento = docx.Document(ruta)
        for parrafo in documento.paragraphs:
            texto += parrafo.text + "\n"
    except Exception as e:
        texto = f"Error al extraer DOCX: {e}"
    return texto

def extraer_texto_excel(ruta):
    """
    Extrae y retorna una representación en texto de un archivo Excel.
    """
    texto = ""
    try:
        df = pd.read_excel(ruta)
        texto = df.to_string()
    except Exception as e:
        texto = f"Error al extraer Excel: {e}"
    return texto

def extraer_texto_documento(ruta):
    """
    Función genérica para extraer texto según la extensión del archivo.
    """
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".pdf":
        return extraer_texto_pdf(ruta)
    elif ext in [".doc", ".docx"]:
        return extraer_texto_docx(ruta)
    elif ext in [".xls", ".xlsx"]:
        return extraer_texto_excel(ruta)
    else:
        return "Formato de archivo no soportado."

# =========================
# FUNCIONES DEL CHAT
# =========================
# Variable global para almacenar el contexto del documento
contexto_documento = ""

def mostrar_pensando():
    """
    Muestra una animación de "Pensando..." mientras se procesa la respuesta.
    """
    for _ in range(3):
        for dots in range(1, 4):
            print(f"🤖 Pensando{'.' * dots}", end="\r")
            time.sleep(0.5)

def chat_con_modelo():
    """
    Función principal del chatbot.
    Permite enviar preguntas, cargar contexto de un documento, ver el historial y salir.
    """
    global contexto_documento  # Variable global para almacenar el contexto
    print("🤖 Chatbot Deepseek - Escribe 'salir' para terminar, 'historial' para ver el historial o 'cargar_contexto' para añadir un documento.")

    while True:
        pregunta = input("Tú: ").strip()
        
        if pregunta.lower() == "salir":
            print("🔚 Chat finalizado.")
            break
        
        elif pregunta.lower() == "historial":
            ver_historial()
            continue
        
        elif pregunta.lower() == "cargar_contexto":
            ruta = input("Ingresa la ruta completa del documento: ").strip()
            contexto_documento = extraer_texto_documento(ruta)
            
            # Recortar el contenido si es muy largo
            MAX_LONGITUD = 2000  # Cantidad máxima de caracteres permitidos
            if len(contexto_documento) > MAX_LONGITUD:
                contexto_documento = contexto_documento[:MAX_LONGITUD] + "\n...[texto recortado]"
            
            # Imprimir los primeros 500 caracteres para verificar el contenido extraído
            print("Contenido extraído del documento (primeros 500 caracteres):")
            print(contexto_documento[:500])
            
            print("✅ Contexto cargado correctamente.")
            continue

        # Guardar la pregunta del usuario en la base de datos
        guardar_mensaje("Usuario", pregunta)

        # Iniciar el hilo para mostrar "Pensando..."
        hilo_pensando = threading.Thread(target=mostrar_pensando)
        hilo_pensando.start()

        # Preparar los mensajes para enviar al modelo, incluyendo el contexto si existe.
        # Se indica de forma explícita que la respuesta debe ser en español.
        mensajes = []
        if contexto_documento:
            mensajes.append({
                "role": "system",
                "content": (
                    "El siguiente documento se usará como contexto en la conversación:\n"
                    f"{contexto_documento}\n\n"
                    "Responde en español de forma clara y concisa basándote en este contexto. "
                    "Por favor, asegúrate de que la respuesta esté en español."
                )
            })
        else:
            mensajes.append({
                "role": "system",
                "content": "Responde en español de forma clara y concisa. Por favor, asegúrate de que la respuesta esté en español."
            })
        # Agregar el mensaje del usuario
        mensajes.append({"role": "user", "content": pregunta})
        
        # Consultar al modelo Mistral a través de Ollama
        respuesta = ollama.chat(
            model="deepseek-r1:7b",
            messages=mensajes
        )


        # Esperar a que la animación termine antes de mostrar la respuesta
        hilo_pensando.join()

        # Extraer y mostrar la respuesta del modelo
        mensaje_respuesta = respuesta['message']['content']
        print(" " * 20, end="\r")  # Limpiar la línea de animación
        print("🤖 Deepseek:", mensaje_respuesta)

        # Guardar la respuesta del modelo en la base de datos
        guardar_mensaje("Deepseek", mensaje_respuesta)

if __name__ == "__main__":
    chat_con_modelo()
