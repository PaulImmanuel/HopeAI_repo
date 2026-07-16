import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.Two_agents.agent import root_agent


APP_NAME = "Two_agent"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def main():

    # -----------------------------------------
    # Session Service
    # -----------------------------------------
    session_service = InMemorySessionService()


    # -----------------------------------------
    # Runner
    # -----------------------------------------
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )


    # -----------------------------------------
    # Create Session
    # -----------------------------------------
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )


    print("\nADK Multi-Agent System Started")
    print("Type 'exit' to quit.\n")


    # -----------------------------------------
    # Chat Loop
    # -----------------------------------------
    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("\nExiting...")
            break


        async for event in runner.run_async(

            user_id=USER_ID,

            session_id=SESSION_ID,

            new_message=types.Content(
                role="user",
                parts=[
                    types.Part(text=user_input)
                ]
            )
        ):

            # -----------------------------------------
            # Final Response
            # -----------------------------------------
            if event.is_final_response():

                if event.content and event.content.parts:

                    print("\nAgent:\n")

                    print(event.content.parts[0].text)

                    print("\n" + "-" * 60 + "\n")


# -----------------------------------------
# Run Application
# -----------------------------------------
asyncio.run(main())