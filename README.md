# Agentes con Google ADK

Prácticas del curso **"Desarrolla agentes con el Kit de desarrollo de agentes (ADK)"** de Google, hechas en Python con [`google-adk`](https://google.github.io/adk-docs/) 2.8 y modelos Gemini a través de la API gratuita de Google AI Studio.

Cada carpeta es un agente independiente que se puede abrir en la interfaz de desarrollo de ADK (`adk web`). El código sigue el material del curso, con las correcciones necesarias para que funcione en la versión actual de ADK y en una cuenta gratuita (ver [Notas](#notas-sobre-el-nivel-gratuito-de-gemini)).

## Prácticas

| Carpeta | Tema | Qué demuestra | Estado |
|---|---|---|---|
| [`my_first_agent`](my_first_agent/) | Primer agente | `LlmAgent` mínimo: modelo, nombre, descripción e instrucción (tutor de álgebra). | ✅ |
| [`model_comparison`](model_comparison/) | Parámetros del modelo | Dos agentes con el mismo modelo y distinta `generate_content_config`: uno factual (`temperature=0.1`) y uno creativo (`temperature=0.9`), con `top_p`, `top_k`, `max_output_tokens` y `safety_settings`. | ✅ |
| [`product_extractor`](product_extractor/) | Salida estructurada | `output_schema` con un modelo Pydantic para obligar una respuesta JSON validada, y `output_key` para guardarla en el estado de la sesión. | ✅ |
| [`namespace_demo`](namespace_demo/) | Estado y memoria | Los cuatro espacios de nombres del estado (`temp:`, sesión, `user:`, `app:`) y su persistencia, con un script que lo verifica usando `Runner` e `InMemorySessionService`. | ✅ |
| [`research_assistant`](research_assistant/) | Herramienta integrada: búsqueda | `google_search`, la herramienta de búsqueda con fundamentación (*grounding*) que provee ADK. | ⚠️ Requiere nivel pago |
| [`math_assistant`](math_assistant/) | Herramienta integrada: código | `BuiltInCodeExecutor`: el modelo escribe y ejecuta Python para calcular con exactitud. | ✅ |
| [`research_assistant_ddg`](research_assistant_ddg/) | Bonus: herramienta personalizada | Misma idea que `research_assistant`, pero con una función propia que busca en DuckDuckGo (gratis) y con reintentos automáticos (`retry_options`). | ✅ |

## Requisitos

- Python 3.11 o superior (desarrollado con 3.13).
- Una API key de Gemini, gratuita, de [Google AI Studio](https://aistudio.google.com/apikey).

## Instalación

```bash
git clone https://github.com/Martin-Mancilla-98/agentes-google-adk.git
cd agentes-google-adk

python -m venv .venv
.venv\Scripts\activate          # Windows (CMD)   |   source .venv/bin/activate  (Linux/macOS)

pip install -r requirements.txt
```

Después, copiar `.env.example` como `.env` **dentro de cada carpeta de agente** que se quiera usar y pegar la API key:

```bash
copy .env.example math_assistant\.env
```

ADK busca el `.env` en la carpeta del agente, no en la raíz.

## Cómo ejecutar

**Interfaz web** (todos los agentes), desde la raíz del repositorio:

```bash
adk web
```

Abrir <http://localhost:8000>, elegir el agente en el desplegable y chatear. La pestaña **Events** muestra cada paso interno: llamadas al modelo, código ejecutado, herramientas invocadas y sus respuestas.

**Script de la práctica de estado**, desde su carpeta:

```bash
cd namespace_demo
python test_namespaces.py
```

Cada carpeta tiene su propio `README.md` con los prompts de prueba y qué observar.

## Estructura de un agente

```
math_assistant/
├── __init__.py     # `from . import agent` — así adk web descubre el agente
├── agent.py        # define `root_agent`
└── .env            # GOOGLE_API_KEY (no se sube; ver .env.example)
```

## Notas sobre el nivel gratuito de Gemini

Cosas que el material del curso da por sentadas y que, en septiembre de 2026 y con una cuenta gratuita nueva, ya no son así:

- **Los modelos `gemini-2.5-*` no están disponibles para cuentas nuevas** (`404: no longer available to new users`). Las prácticas usan `gemini-3.5-flash`, `gemini-3.5-flash-lite` y `gemini-3.6-flash`.
- **La búsqueda de Google (`google_search`) no tiene cuota en el nivel gratuito** para los modelos Gemini 3.x: devuelve `429 RESOURCE_EXHAUSTED` en la primera llamada. Solo funciona con facturación activada. Por eso `research_assistant` queda como código de referencia y existe `research_assistant_ddg`.
- **La ejecución de código (`BuiltInCodeExecutor`) sí es gratuita**: se cobra como tokens normales, que en el nivel gratuito no tienen costo.
- **ADK no reintenta por defecto**: un `503 UNAVAILABLE` por alta demanda corta la respuesta. `research_assistant_ddg` muestra cómo activar reintentos con `Gemini(retry_options=HttpRetryOptions(...))`.

## Diferencias con el material del curso

Correcciones que hubo que hacer para que los ejemplos funcionaran en ADK 2.8:

- En las instrucciones, la sintaxis para variables de estado opcionales es `{clave?}` (vacío si no existe). La forma `{clave?valor_por_defecto}` que aparece en el material no está soportada y queda como texto literal.
- `create_session()` devuelve una **copia** de la sesión: asignar `session.state["x"] = ...` sobre ella no llega al almacenamiento. El estado inicial se pasa con `create_session(state={...})`, y después de cada turno hay que volver a pedir la sesión con `get_session()`.
- Las claves `temp:` se descartan del estado inicial. Para demostrarlas se pasan en el turno con `runner.run_async(..., state_delta={"temp:step": ...})`.
- `create_session()` y `get_session()` son asíncronas; el script de prueba usa `asyncio`.
- Al crear un proyecto con `adk create`, elegir el backend **1 (Google AI)**. Las opciones 2 y 3 configuran Vertex AI, que requiere Google Cloud con facturación.

## Licencia

Código de práctica, de uso libre. El material del curso pertenece a Google y no se incluye.
