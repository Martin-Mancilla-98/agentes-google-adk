# file_reader_assistant — Herramientas MCP (Model Context Protocol)

Asistente que lista y lee archivos usando un **servidor MCP ya existente**: [`@modelcontextprotocol/server-filesystem`](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem). El agente no tiene ninguna herramienta escrita en Python: ADK se conecta al servidor, le pregunta qué herramientas ofrece y se las pasa al modelo.

```python
McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem@2026.8.31", ALLOWED_PATH],
        ),
    ),
    tool_filter=["list_directory", "read_text_file"],  # solo lectura
)
```

## Qué demuestra

- **MCP como adaptador universal**: el mismo servidor funciona con ADK, Claude, GPT o cualquier cliente compatible. Integrarlo es conectar y configurar, no escribir código.
- **`McpToolset`**: se agrega a `tools` como cualquier herramienta, lanza el servidor, descubre sus herramientas automáticamente y hace de intermediario en cada llamada.
- **`StdioConnectionParams`**: el servidor corre como subproceso local (`npx`) y se comunica por entrada/salida estándar. Para servidores remotos existen `SseConnectionParams` y `StreamableHTTPConnectionParams`.
- **`tool_filter` como medida de seguridad**: el servidor ofrece 14 herramientas, incluidas `write_file`, `edit_file` y `move_file`. El filtro deja pasar solo dos de lectura, así que el modelo ni siquiera sabe que las otras existen.
- **Aislamiento por carpeta**: el servidor solo acepta rutas dentro del directorio que recibe como argumento (`my_files/`).

## Requisitos

- Soporte MCP de ADK, que es opcional: `pip install "google-adk[mcp]==2.8.0"` (ya incluido en `requirements.txt`).
- [Node.js](https://nodejs.org/), que trae `npx`. Desarrollado con Node 24.

Opcional, pero evita que la primera ejecución tarde: descargar el servidor una vez y cortarlo con `Ctrl+C` cuando diga *"Secure MCP Filesystem Server running on stdio"*.

```bash
npx -y @modelcontextprotocol/server-filesystem@2026.8.31 .
```

## Probar

```bash
adk web
```

Elegir `file_reader_assistant`:

- `¿Qué archivos hay en la carpeta?` → llama a `list_directory` → `[FILE] hello.txt`, `[FILE] notes.txt`
- `Muéstrame el contenido de hello.txt` → llama a `read_text_file`
- `Enumera los archivos y, a continuación, lee el archivo notes.txt` → encadena las dos herramientas (si la lista ya salió antes en la misma conversación, el modelo puede reutilizarla y llamar solo a `read_text_file`)
- `Crea un archivo nuevo llamado prueba.txt` → se niega: `write_file` existe en el servidor pero el filtro no se la expone.

Qué observar: en **Events**, los `functionCall` y `functionResponse` son iguales a los de una herramienta propia (ver `research_assistant_ddg`), pero acá nadie las escribió en el proyecto. En la consola de `adk web` aparece el mensaje de arranque del servidor MCP.

## Diferencias con el material del curso

| Material del curso | Acá | Por qué |
|---|---|---|
| `os.path.abspath("./my_files")` | Ruta calculada desde `__file__` | `abspath` depende del directorio desde donde se ejecuta `adk web` (la raíz del repo), así que la carpeta se creaba fuera del agente. |
| `tool_filter=['list_directory', 'read_file']` | `read_text_file` | `read_file` está marcada como obsoleta en el servidor actual. |
| `@modelcontextprotocol/server-filesystem` | Versión fijada `@2026.8.31` | Evita que una actualización del servidor cambie los nombres de las herramientas sin aviso, como pasó con `read_file`. |
| Timeout por defecto | `timeout=30` | ADK espera 5 segundos a que el servidor arranque; la primera vez `npx` tiene que descargar el paquete y no alcanza. |
| Sin `cwd` y ruta sin mencionar | `cwd=ALLOWED_PATH` y la ruta absoluta en la instrucción | El servidor resuelve las rutas relativas contra su directorio de trabajo. Sin esto, un `hello.txt` a secas apunta fuera de la carpeta permitida y devuelve *Access denied*. |
| `gemini-2.5-flash` | `gemini-3.5-flash` con `retry_options` | Ver las notas del README principal. |

En Windows, `adk web` avisa que desactiva `--reload`: es necesario para que pueda lanzar subprocesos como el servidor MCP, y no requiere hacer nada.
