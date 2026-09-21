# math_assistant — Herramienta integrada de ejecución de código

Asistente de matemáticas que, en vez de "estimar" resultados, **escribe y ejecuta Python** para calcularlos.

```python
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = LlmAgent(..., code_executor=BuiltInCodeExecutor())
```

## Qué demuestra

- La ejecución de código se activa con el parámetro `code_executor`, **no** dentro de la lista `tools`.
- El código corre en el entorno aislado de Google, no en la máquina local.
- Resultados exactos y verificables: el código generado y su salida quedan registrados en los eventos.
- Es gratuita en el nivel gratuito de la API (se cobra solo como tokens).

## Probar

```bash
adk web
```

Elegir `math_assistant`:

- `Calcula una propina del 15% en una factura de $87.50` → `13.13`
- `¿Cuál es el interés compuesto de $5,000 invertidos a una tasa anual del 6% durante 8 años, con capitalización mensual?`
- `Calcula el promedio, la mediana y la desviación estándar de estos números: 12, 15, 18, 20, 22, 25, 28, 30`

Qué observar: en la pestaña **Events**, la respuesta del agente contiene dos partes además del texto: `executable_code` (el Python que escribió el modelo) y `code_execution_result` (la salida de ejecutarlo).

## Nota

Si aparece `503 UNAVAILABLE — This model is currently experiencing high demand`, es un pico transitorio del lado de Google: reintentar. Para que el agente reintente solo, ver `retry_options` en [`research_assistant_ddg`](../research_assistant_ddg/agent.py).
