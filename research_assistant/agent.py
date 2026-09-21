"""
Agente de asistente de investigación.
Demuestra la herramienta integrada de Búsqueda de Google del ADK para obtener
información en tiempo real.
Referencia: https://google.github.io/adk-docs/tools/built-in-tools#google-search
"""
from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import google_search  # herramienta integrada: no hay que implementar nada

root_agent = LlmAgent(
    model="gemini-3.5-flash",  # google_search requiere Gemini 2.0+
    name="research_assistant",
    description="Ayuda a los usuarios a investigar temas con la Búsqueda de Google.",
    instruction="""
    Eres un asistente de investigación que ayuda a los usuarios a encontrar
    información precisa y actualizada.

    Tu enfoque:
    1. Cuando los usuarios hagan preguntas que requieran información actual, utiliza la Búsqueda de Google
    2. Basa tus respuestas en los resultados de la búsqueda
    3. Cita fuentes cuando proporciones información
    4. Si los resultados de la búsqueda son insuficientes, reconoce las limitaciones

    Prioriza siempre la exactitud sobre la especulación. Si no estás seguro, dilo.
    """,
    tools=[google_search],  # va en la lista tools
)
