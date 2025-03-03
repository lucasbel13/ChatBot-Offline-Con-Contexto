# Chatbot Offline con Contexto

Este proyecto es un chatbot desarrollado en Python para Windows 11 que se ejecuta en VS Code. Utiliza un modelo LLM a través de la API de Ollama (por ejemplo, Deepseek o Mistral) y permite cargar documentos (PDF, Word, Excel) para extraer texto y usarlo como contexto en las conversaciones. Además, almacena el historial de chat en una base de datos MySQL.

## Características

- **Conversación en español:** El bot responde de forma clara y concisa en español.
- **Carga de contexto:** Puedes cargar documentos en formatos PDF, DOCX y Excel para enriquecer las respuestas del bot.
- **Historial de mensajes:** Guarda el historial de conversaciones en una base de datos MySQL.
- **Animación de "Pensando...":** Se muestra una animación mientras se procesa la respuesta.

## Requisitos

- **Python 3.11** (o superior)
- **MySQL Server**  
  - Base de datos: `chatbot`
  - Tabla: `historial_chat`
- **Dependencias de Python:**
  - `ollama`
  - `mysql-connector-python`
  - `PyPDF2`
  - `python-docx`
  - `pandas`
  - `openpyxl`

Puedes instalar las dependencias ejecutando:

```bash
pip install ollama mysql-connector-python PyPDF2 python-docx pandas openpyxl
Instalación
Clona el repositorio:

bash

git clone https://github.com/tu_usuario/nombre_del_repositorio.git
Accede a la carpeta del proyecto:

bash

cd nombre_del_repositorio
Instala las dependencias:

bash

pip install -r requirements.txt
Nota: Asegúrate de crear el archivo requirements.txt con las dependencias o instala cada paquete individualmente.

Configura la base de datos MySQL:

Crea la base de datos chatbot.

Crea la tabla historial_chat ejecutando:

sql

CREATE TABLE historial_chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    mensaje TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Asegúrate de que la base de datos y la tabla usen el conjunto de caracteres utf8mb4 para soportar emojis y otros caracteres Unicode:

sql

ALTER DATABASE chatbot CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE historial_chat CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Uso
Ejecuta el script principal:

bash

python Chatbot_Offline_con_Contexto.py
Comandos disponibles en el chat:

Escribe salir para terminar la conversación.
Escribe historial para ver los últimos mensajes almacenados.
Escribe cargar_contexto para cargar un documento y usar su contenido como contexto en la conversación.
Cambio de modelo:
Para cambiar el modelo LLM, modifica el parámetro model en la llamada a ollama.chat() en el código.

Personalización
Extensiones: Puedes ampliar el soporte para otros formatos de documentos.
Ajuste de respuestas: Modifica el mensaje del sistema para personalizar las respuestas del bot.
