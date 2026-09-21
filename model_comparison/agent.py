from google.adk.agents import LlmAgent
from google.genai import types

# Agente 1: Optimizado para la extracción de datos fácticos
factual_agent = LlmAgent(
    model="gemini-3.5-flash-lite",
    name="data_extractor",
    description="Extrae información fáctica de forma sumamente coherente",
    instruction="""Eres un extractor de datos precisos.
Extrae hechos exactamente como se indica. No hagas lo siguiente:
- Agregar información que no figure en la entrada
- Hacer suposiciones o inferencias
- Usar lenguaje creativo
Sé preciso, conciso y deterministico.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        max_output_tokens=500,
        top_p=0.8,
        top_k=10,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ],
    ),
)

# Agente 2: Optimizado para la generación de ideas creativas
creative_agent = LlmAgent(
    model="gemini-3.5-flash-lite",
    name="creative_brainstormer",
    description="Genera ideas creativas y explora posibilidades",
    instruction="""Eres un socio de generación de ideas creativo.
Genera ideas innovadoras, diversas y originales. Puedes hacer lo siguiente:
- Pensar de forma creativa
- Combinar conceptos inesperados
- Explorar enfoques no convencionales
Sé creativo, ofrece distintas opciones y fomenta la reflexión.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=2000,
        top_p=0.95,
        top_k=40,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            )
        ],
    ),
)

# Agente activo para probar primero
root_agent = creative_agent