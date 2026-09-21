"""
Asistente de investigación con búsqueda web GRATUITA (DuckDuckGo).

Variante de `research_assistant`: la herramienta integrada `google_search` del ADK
no está disponible en el nivel gratuito de la API de Gemini para los modelos 3.x
(responde 429 RESOURCE_EXHAUSTED en la primera llamada). Acá la búsqueda se
implementa como HERRAMIENTA PERSONALIZADA: una función de Python que ADK expone
al modelo a partir de su firma y su docstring.

Referencia: https://google.github.io/adk-docs/tools/function-tools
"""
from ddgs import DDGS
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def buscar_web(consulta: str, max_resultados: int = 5) -> dict:
    """Busca en la web con DuckDuckGo y devuelve los resultados principales.

    Usá esta herramienta cuando necesites información actual o que no conozcas
    con certeza. Podés llamarla varias veces con consultas distintas.

    Args:
        consulta: Texto a buscar (en cualquier idioma).
        max_resultados: Cantidad máxima de resultados a devolver (1 a 10).

    Returns:
        Un dict con 'status' ('ok' o 'error'). Si es 'ok', incluye 'resultados':
        una lista de dicts con 'titulo', 'url' y 'resumen'. Si es 'error',
        incluye 'mensaje' con la causa.
    """
    cantidad = max(1, min(max_resultados, 10))
    try:
        hits = DDGS().text(consulta, max_results=cantidad)
    except Exception as e:  # p. ej. límite de peticiones de DuckDuckGo
        return {"status": "error", "mensaje": str(e)}

    return {
        "status": "ok",
        "resultados": [
            {"titulo": h.get("title"), "url": h.get("href"), "resumen": h.get("body")}
            for h in hits
        ],
    }


root_agent = LlmAgent(
    # Por defecto ADK NO reintenta: un 503 ("alta demanda") o un 429 (límite por
    # minuto) del nivel gratuito cortan la respuesta. Con retry_options la llamada
    # se reintenta sola hasta 5 veces con espera creciente (2 s, 4 s, 8 s, 16 s).
    model=Gemini(
        model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(attempts=5, initial_delay=2, max_delay=30),
    ),
    name="research_assistant_ddg",
    description="Asistente de investigación que busca en la web con DuckDuckGo.",
    instruction="""
    Eres un asistente de investigación que ayuda a los usuarios a encontrar
    información precisa y actualizada.

    Tu enfoque:
    1. Cuando el usuario pregunte algo que requiera información actual, usa la
       herramienta buscar_web. No respondas de memoria sobre hechos recientes.
    2. Basa tus respuestas en los resultados de la búsqueda.
    3. Cita las fuentes: incluye el título y la URL de los resultados que usaste.
    4. Si la búsqueda devuelve status 'error' o resultados insuficientes,
       reconoce la limitación en lugar de inventar.

    Prioriza siempre la exactitud sobre la especulación. Si no estás seguro, dilo.
    """,
    tools=[buscar_web],  # función propia -> ADK la convierte en FunctionTool
)
