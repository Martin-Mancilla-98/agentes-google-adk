# my_first_agent — Primer agente

El `LlmAgent` más simple posible: modelo, nombre, descripción e instrucción. Un tutor de álgebra paciente.

## Qué demuestra

- La estructura mínima de un agente ADK: `agent.py` con un `root_agent`, `__init__.py` que lo importa y `.env` con la credencial.
- Cómo la `instruction` define la personalidad y el alcance del agente.

## Probar

```bash
adk web
```

Elegir `my_first_agent` y preguntar, por ejemplo:

- `¿Cómo resuelvo 2x + 3 = 11?`
- `No entiendo qué es una ecuación lineal`

Qué observar: guía paso a paso en lugar de dar la respuesta directa, como pide la instrucción.
