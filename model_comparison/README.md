# model_comparison — Parámetros de generación

Dos agentes con el **mismo modelo** y configuraciones opuestas de `generate_content_config`, para ver cómo los parámetros cambian el comportamiento:

| Agente | `temperature` | `top_p` | `top_k` | `max_output_tokens` | Uso |
|---|---|---|---|---|---|
| `factual_agent` (`data_extractor`) | 0.1 | 0.8 | 10 | 500 | Extraer hechos sin inventar |
| `creative_agent` (`creative_brainstormer`) | 0.9 | 0.95 | 40 | 2000 | Generar ideas variadas |

Además, cada uno tiene un `safety_settings` distinto para la categoría `DANGEROUS_CONTENT`.

## Qué demuestra

- `temperature` baja → respuestas cortas, repetibles y literales; alta → respuestas largas y distintas en cada ejecución.
- `top_p` / `top_k` acotan de cuántos candidatos elige el modelo cada palabra.
- `max_output_tokens` limita el largo de la respuesta.

## Probar

Solo un agente puede ser `root_agent`. Por defecto está activo el creativo; para probar el factual, cambiar la última línea de `agent.py`:

```python
root_agent = factual_agent
```

Luego `adk web`, elegir `model_comparison` y usar el **mismo prompt** con ambos, por ejemplo:

- `Dame tres usos para un ladrillo`
- `¿Cuál es la capital de Australia?`

Qué observar: repetir el mismo prompt varias veces. El factual responde casi igual siempre; el creativo cambia cada vez.
