"""
Prueba los espacios de nombres de estado para ver las diferencias de persistencia.
Ejecutar desde la carpeta namespace_demo:  python test_namespaces.py
"""
import asyncio

from dotenv import load_dotenv
load_dotenv()  # `adk web` carga el .env solo; `python` no, por eso va acá

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP = "namespace_demo_app"
USER = "user1"
CLAVES = ("temp:step", "topic", "user:theme", "app:version")


async def chat(runner, session_id, texto, state_delta=None):
    msg = Content(role="user", parts=[Part(text=texto)])
    async for event in runner.run_async(
        user_id=USER, session_id=session_id, new_message=msg, state_delta=state_delta
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Respuesta del agente:\n{event.content.parts[0].text}\n")


async def mostrar_estado(service, session_id, titulo):
    # Siempre pedir la sesión fresca al servicio: el objeto viejo es una copia stale
    s = await service.get_session(app_name=APP, user_id=USER, session_id=session_id)
    print(f"=== {titulo} ===")
    print(f"Estado completo: {s.state}")
    for k in CLAVES:
        print(f"  {k}: {s.state.get(k)}")
    print()


async def main():
    service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP, session_service=service)

    print("=== Estableciendo el estado en todos los espacios de nombres ===")
    session = await service.create_session(
        app_name=APP, user_id=USER, session_id="session1",
        state={
            "app:name": "Demostración de espacios de nombres",
            "app:version": "2.0",
            "user:theme": "dark",
            "topic": "state management",
        },
    )
    print(f"Estado previo a la ejecución: {session.state}\n")

    print("=== Agente en ejecución (turno 1, con temp:step) ===")
    await chat(runner, "session1", "Muéstrame los valores de los espacios de nombres",
               state_delta={"temp:step": "initialization"})
    await mostrar_estado(service, "session1", "Estado posterior al turno 1")

    print("=== Turno 2 (misma sesión, sin temp:step) ===")
    await chat(runner, "session1", "Vuelve a verificar el estado")
    await mostrar_estado(service, "session1", "Estado posterior al turno 2")

    print("=== NUEVA sesión (session2), mismo usuario ===")
    await service.create_session(app_name=APP, user_id=USER, session_id="session2")
    await mostrar_estado(service, "session2", "Estado de la nueva sesión")


asyncio.run(main())
