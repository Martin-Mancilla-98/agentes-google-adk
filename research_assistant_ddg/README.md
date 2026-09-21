# research_assistant_ddg — Búsqueda web gratis con una herramienta personalizada

Variante de [`research_assistant`](../research_assistant/) que **sí funciona con la cuenta gratuita**: en lugar de la herramienta integrada `google_search`, la búsqueda es una función de Python propia que consulta DuckDuckGo con la librería [`ddgs`](https://pypi.org/project/ddgs/) (sin API key).

```python
def buscar_web(consulta: str, max_resultados: int = 5) -> dict:
    """Busca en la web con DuckDuckGo y devuelve los resultados principales. ..."""
    ...

root_agent = LlmAgent(..., tools=[buscar_web])
```

## Qué demuestra

- **Herramienta personalizada (`FunctionTool`)**: ADK construye la descripción que ve el modelo a partir de la firma de la función (nombres y tipos de parámetros) y su docstring. Por eso el docstring está escrito "para el modelo": cuándo usarla, qué devuelve.
- El modelo decide solo cuándo llamarla y con qué consulta; puede llamarla varias veces en una misma respuesta.
- Devolver un `dict` con `status` permite que el agente distinga un error (por ejemplo, límite de peticiones de DuckDuckGo) y lo comunique en vez de inventar.
- **Reintentos automáticos**: ADK no reintenta por defecto, así que un `503` por alta demanda corta la respuesta. Se activa con:

  ```python
  from google.adk.models.google_llm import Gemini
  from google.genai import types

  model=Gemini(
      model="gemini-3.5-flash",
      retry_options=types.HttpRetryOptions(attempts=5, initial_delay=2, max_delay=30),
  )
  ```

  `attempts` es el total de intentos (incluido el primero); la espera arranca en `initial_delay` segundos y se duplica en cada reintento (2, 4, 8, 16 s) sin superar `max_delay`. Solo reintenta errores transitorios (408, 429, 500, 502, 503, 504).

## Probar

Requiere `ddgs` (incluido en `requirements.txt`).

```bash
adk web
```

Elegir `research_assistant_ddg`:

- `¿Quién es el actual director general de Microsoft?`
- `Compara vehículos eléctricos y vehículos de pila de combustible de hidrógeno`

Qué observar: en **Events** aparecen dos eventos que las herramientas integradas no generan: `functionCall` (el modelo pidiendo `buscar_web` con la consulta que eligió) y `functionResponse` (los resultados que devolvió DuckDuckGo). La respuesta final cita título y URL de las fuentes.

## Diferencia conceptual con la lección

| | Herramienta integrada (`google_search`) | Herramienta personalizada (`buscar_web`) |
|---|---|---|
| Implementación | La provee Google | La escribe uno |
| Mantenimiento | ADK | Propio |
| Costo | Nivel pago | Gratis |
| Combinable con otras herramientas | No (una sola por agente) | Sí |
