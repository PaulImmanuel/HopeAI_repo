from dotenv import load_dotenv

# Load environment variables
load_dotenv()


from google.adk.agents import Agent


# -----------------------------
# Tool Function
# -----------------------------
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.
    """
    return a * b


# -----------------------------
# Root Agent
# -----------------------------
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


root_agent = LlmAgent(
    model="gemini-3.1-flash-lite",
    name="gemini_agent",
    instruction="""
You are a helpful Math AI assistant.
""",tools=[multiply]
)