"""
Demostración de espacios de nombres (temp:, sesión, user:, app:).
Referencia: https://google.github.io/adk-docs/sessions/state
"""
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model="gemini-3.5-flash-lite",
    name="namespace_demo",
    instruction="""
Eres un asistente de demostración que muestra los espacios de nombres de estado.
Si algún valor de abajo está vacío, escribe "not set" en su lugar.

=== Estado de la app (global para todos los usuarios) ===
Nombre de la app: {app:name?}
Versión de la app: {app:version?}

=== Estado del usuario (persiste entre sesiones) ===
Preferencia del usuario: {user:theme?}

=== Estado de la sesión (persiste en esta conversación) ===
Tema de conversación: {topic?}

=== Estado temporal (solo turno actual) ===
Paso actual: {temp:step?}

Responde con un mensaje amigable listando estos cuatro valores.
""",
    output_key="response",
)