"""
Agente asistente de lectura de archivos.
Demuestra la integración de herramientas MCP en ADK usando el servidor MCP
del sistema de archivos (@modelcontextprotocol/server-filesystem).

Referencia: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""
import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.genai import types
from mcp import StdioServerParameters

# Carpeta a la que el servidor MCP tiene acceso (debe ser una ruta absoluta).
# Se calcula a partir de ESTE archivo y no del directorio desde donde se ejecuta
# `adk web`, así siempre apunta a file_reader_assistant/my_files.
ALLOWED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_files")
os.makedirs(ALLOWED_PATH, exist_ok=True)

root_agent = LlmAgent(
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=5, initial_delay=2, max_delay=30),
    ),
    name="file_reader_assistant",
    description="Ayuda a los usuarios a leer y explorar archivos con las herramientas del MCP.",
    instruction=f"""
    Eres un asistente de lectura de archivos que ayuda a los usuarios a explorar archivos.

    Trabajas SOLO dentro de esta carpeta: {ALLOWED_PATH}
    Al llamar a las herramientas, usa siempre rutas absolutas dentro de ella.

    Tus capacidades:
    - Mostrar una lista de archivos en los directorios con list_directory
    - Leer el contenido de un archivo con read_text_file

    Cuando ayudes a los usuarios:
    1. Utiliza list_directory para mostrar los archivos disponibles.
    2. Utiliza read_text_file para mostrar el contenido del archivo cuando se te solicite.
    3. Describe lo que encuentras de una manera útil.

    Expresa con claridad cuál es la carpeta con la que estás trabajando.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem@2026.8.31",
                        ALLOWED_PATH,
                    ],
                    cwd=ALLOWED_PATH,  # las rutas relativas se resuelven dentro de my_files
                ),
                timeout=30,  # por defecto son 5 s; alcanza para que arranque npx
            ),
            # Solo herramientas de lectura. read_file está obsoleta: se usa read_text_file.
            tool_filter=["list_directory", "read_text_file"],
        )
    ],
)