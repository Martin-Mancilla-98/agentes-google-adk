"""
Agente asistente de matemáticas.
Demuestra la herramienta integrada de ejecución de código del ADK para realizar
cálculos precisos.
Referencia: https://google.github.io/adk-docs/tools/built-in-tools#code-execution
"""
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor  # ejecutor de código integrado

root_agent = LlmAgent(
    model="gemini-3.5-flash",  # la ejecución de código requiere Gemini 2.0+
    name="math_assistant",
    description="Ayuda a los usuarios con cálculos y análisis matemáticos.",
    instruction="""
    Eres un asistente de matemáticas que ayuda a los usuarios con cálculos y análisis matemáticos.

    Tus capacidades:
    1. Cuando los usuarios pidan cálculos, utiliza la ejecución de código para mayor precisión.
    2. Muestra tu trabajo explicando los pasos del cálculo.
    3. Verifica los resultados ejecutando el código.
    4. Realiza operaciones matemáticas complejas (estadísticas, álgebra, etc.).

    Utiliza siempre la ejecución de código para cálculos numéricos para garantizar la exactitud.
    """,
    code_executor=BuiltInCodeExecutor(),  # OJO: va en code_executor, NO en tools
)
