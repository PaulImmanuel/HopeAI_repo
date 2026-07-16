from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


# -----------------------------------------
# Shared Model
# -----------------------------------------
MODEL = LiteLlm(
    model="gemini/gemini-3.1-flash-lite"
)


# -----------------------------------------
# Research Agent
# -----------------------------------------
research_agent = LlmAgent(
    name="research_agent",

    model=MODEL,

    description="Research specialist",

    instruction="""
You are a research specialist.

ONLY do:
- topic analysis
- research
- technical explanations

Always provide a direct helpful answer.
Never refuse.
"""
)


# -----------------------------------------
# Content Agent
# -----------------------------------------
content_agent = LlmAgent(
    name="content_agent",

    model=MODEL,

    description="Content writer specialist",

    instruction="""
You are a professional content writer.

ONLY do:
- blog writing
- content writing
- beginner explanations
- article formatting

Always provide final content.
Never refuse.
"""
)


# -----------------------------------------
# Supervisor Agent
# -----------------------------------------
root_agent = LlmAgent(
    name="supervisor_agent",

    model=MODEL,

    description="Routes tasks to correct agents",

    instruction="""
You are a supervisor agent.

Rules:
- NEVER answer directly.
- ALWAYS delegate.

Delegation Rules:
- Research/analysis/technical topics → research_agent
- Writing/blog/content creation → content_agent

After delegation:
- allow the delegated agent to complete the task.
- do not interrupt.
- do not apologize.
- do not say you cannot help.
""",

    sub_agents=[
        research_agent,
        content_agent
    ]
)