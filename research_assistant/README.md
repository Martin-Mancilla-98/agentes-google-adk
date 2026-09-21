# research_assistant — Herramienta integrada `google_search`

Asistente de investigación que usa la búsqueda de Google con fundamentación (*grounding*), tal como la provee ADK: se importa y se agrega a `tools`, sin implementar nada.

```python
from google.adk.tools import google_search

root_agent = LlmAgent(..., tools=[google_search])
```

## Qué demuestra

- Cómo se usa una **herramienta integrada**: importar y listar en `tools`.
- La restricción de ADK: **una sola herramienta integrada por agente**, y no se puede combinar con herramientas personalizadas ni con `code_executor` en el mismo agente.
- La obligación de la política de Google: si la respuesta trae sugerencias de búsqueda (`rendered_content`), la aplicación debe mostrarlas.

## ⚠️ Estado: requiere nivel pago

Con una cuenta gratuita de Google AI Studio y modelos Gemini 3.x, la búsqueda de Google **no tiene cuota**: la primera llamada devuelve

```
429 RESOURCE_EXHAUSTED — You exceeded your current quota
```

No es un problema de configuración ni de límite alcanzado; la cuota del nivel gratuito para esta herramienta es cero (los modelos 2.5, que sí la tenían, ya no están disponibles para cuentas nuevas). Funciona únicamente con facturación activada en el proyecto.

El código se mantiene como referencia de la lección. Para un asistente de investigación que funcione gratis, ver [`research_assistant_ddg`](../research_assistant_ddg/).

## Prompts previstos por la lección

- `¿Quién es el actual director general de Microsoft?`
- `¿Cuáles son los avances más recientes en energía renovable?`
- `Compara vehículos eléctricos y vehículos de pila de combustible de hidrógeno`

> Nota: VS Code (Pylance) puede marcar el import de `google_search` con la advertencia *"is not exported from module"*. Es un falso positivo: `google.adk.tools` carga sus herramientas de forma perezosa y define `__all__` dinámicamente, cosa que el analizador estático no puede evaluar. El import funciona.
