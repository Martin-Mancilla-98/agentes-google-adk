# namespace_demo — Espacios de nombres del estado

Un agente cuya instrucción lee cuatro variables de estado con distinto alcance, y un script que comprueba cuánto vive cada una.

| Prefijo | Alcance | Se pierde cuando… | Ejemplo |
|---|---|---|---|
| `temp:` | La invocación actual (un turno) | termina el turno | `temp:step` |
| *(ninguno)* | La sesión (una conversación) | termina la sesión | `topic` |
| `user:` | Todas las sesiones del mismo usuario | nunca (con almacenamiento persistente) | `user:theme` |
| `app:` | Toda la aplicación, todos los usuarios | nunca | `app:version` |

## Qué demuestra

- Cómo inyectar estado en la instrucción con plantillas: `{app:name?}`, `{user:theme?}`, `{topic?}`, `{temp:step?}`. El `?` hace la variable opcional (vacía si no existe).
- Cómo `InMemorySessionService` separa internamente el estado de app, de usuario y de sesión, y por qué una sesión nueva del mismo usuario conserva `user:` y `app:` pero no `topic`.

## Probar

Desde esta carpeta (el script importa `agent.py` de forma relativa):

```bash
cd namespace_demo
python test_namespaces.py
```

Qué observar en la salida:

1. Turno 1: el agente ve `temp:step = initialization`. Después del turno, `temp:step` es `None`.
2. Turno 2 (misma sesión): `topic`, `user:theme` y `app:version` siguen; `temp:step` no.
3. Sesión nueva (`session2`, mismo usuario): `topic` es `None`; `user:theme` y `app:version` persisten.

## Notas de implementación

El script se aparta del material del curso en tres puntos (ver el README principal): el estado inicial se pasa con `create_session(state=...)` porque el objeto devuelto es una copia; `temp:step` se inyecta con `state_delta` en `run_async` porque las claves `temp:` se descartan del estado inicial; y el estado se relee con `get_session()` tras cada turno.

Con `InMemorySessionService`, `user:` y `app:` persisten solo mientras el proceso vive. Para que sobrevivan a un reinicio hace falta `DatabaseSessionService`.
