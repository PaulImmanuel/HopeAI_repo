import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.SingleAgent_Maths.agent import root_agent


APP_NAME = "SingleAgent_Maths"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def main():

    # Create session service
    session_service = InMemorySessionService()

    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Create session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    print("Type 'exit' to quit.\n")

    # LOOP
    while True:

        # User input
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Chat ended.")
            break

        # Run agent
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )
        ):

            # Final response
            if event.is_final_response():

                if event.content and event.content.parts:
                    print("\nAgent:\n")
                    print(event.content.parts[0].text)
                    print()


# Run async app
asyncio.run(main())