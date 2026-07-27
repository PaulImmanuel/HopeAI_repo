import os
import re
import sys
import json
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is not set in environment!")
else:
    logger.info(f"GEMINI_API_KEY is set (length: {len(GEMINI_API_KEY)})")

try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()
except Exception as e:
    logger.error(f"Failed to load knowledge.txt: {e}")
    knowledge = "No knowledge base available."

try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt_template = f.read()
except Exception as e:
    logger.error(f"Failed to load system_prompt.txt: {e}")
    system_prompt_template = "You are the AI assistant for this company."

# Build searchable knowledge sections
knowledge_sections = []
for section in knowledge.split("\n========================================"):
    section = section.strip()
    if not section:
        continue
    lines = section.split("\n")
    label = lines[0].strip("=\n ") if lines else ""
    keywords = set(re.findall(r"[A-Za-z]{3,}", section.lower()))
    knowledge_sections.append({
        "label": label,
        "text": section,
        "keywords": keywords,
    })


def _find_relevant_sections(user_message, top_n=3):
    user_words = set(re.findall(r"[A-Za-z]{3,}", user_message.lower()))
    if not user_words:
        return []
    scored = []
    for sec in knowledge_sections:
        score = len(user_words & sec["keywords"])
        if score > 0:
            scored.append((score, sec))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s["text"] for _, s in scored[:top_n]]


def _knowledge_fallback(user_message):
    sections = _find_relevant_sections(user_message, top_n=1)
    if sections:
        sentences = re.split(r'(?<=[.!?])\s+', sections[0])[:4]
        return " ".join(sentences)

    msg_lower = user_message.lower()
    if any(w in msg_lower for w in ["hello", "hi", "hey", "greetings"]):
        return "Hello! Welcome to PaulTech. How can I assist you today?"
    if any(w in msg_lower for w in ["services", "offer", "do you do", "what can you"]):
        return "PaulTech offers AI Solutions, Web Development, Mobile App Development, Cloud & DevOps, UI/UX Design, and Digital Marketing. Email contact@paultech.io for details."
    if any(w in msg_lower for w in ["price", "cost", "how much", "pricing", "charge"]):
        return "Hourly rates: Junior $40\u2013$60/hr, Senior $110\u2013$150/hr, AI Engineer $130\u2013$180/hr. Websites from $3,000; apps from $10,000. Email sales@paultech.io for a quote."
    if any(w in msg_lower for w in ["contact", "email", "phone", "reach", "call"]):
        return "Email: contact@paultech.io | Phone: +1 (415) 987-6543 | WhatsApp: +1 (415) 987-6543"
    if any(w in msg_lower for w in ["hour", "time", "open", "working", "available"]):
        return "Monday to Friday, 9 AM \u2013 6 PM (PST). 24/7 support for enterprise clients under SLA."
    if any(w in msg_lower for w in ["location", "address", "where", "office", "headquarters"]):
        return "HQ: 100 Technology Drive, Suite 400, San Francisco, CA 94105. Offices: New York, London, Bangalore, Dubai."
    if any(w in msg_lower for w in ["hire", "job", "career", "join", "apply"]):
        return "We are hiring! Roles: Senior AI Engineer, Full Stack Dev, Flutter Dev, DevOps, UX/UI Designer. Apply at www.paultech.io/careers"
    if any(w in msg_lower for w in ["ceo", "founder", "leadership", "team", "john smith"]):
        return "CEO: John Smith (ex-Google VP). CTO: Sarah Chen (PhD CMU). COO: Michael Davis (Wharton). Team: 120+ professionals."
    if any(w in msg_lower for w in ["quote", "estimate", "proposal", "consultation", "free"]):
        return "Free 30-min consultation! Book at www.paultech.io/book-call or email contact@paultech.io."

    return "I'm your PaulTech assistant. Ask me about our services, pricing, team, careers, or contact details."


# --- MULTIPROCESSING WORKER ---


def get_response(user_message):

    relevant = _find_relevant_sections(user_message, top_n=3)

    slim_knowledge = (
        "\n\n---\n\n".join(relevant)
        if relevant
        else knowledge[:3000]
    )

    slim_prompt = (
        f"{system_prompt_template}\n\n"
        f"Answer using ONLY the company knowledge below.\n\n"
        f"Company Knowledge:\n{slim_knowledge}\n\n"
        f"User: {user_message}\nAssistant:"
    )

    if not GEMINI_API_KEY:
        return _knowledge_fallback(user_message)

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        MODELS = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
        ]

        for model in MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=slim_prompt,
                )

                if response.text:
                    return response.text

            except Exception:
                continue

        return _knowledge_fallback(user_message)

    except Exception as e:
        logger.error(e)
        return _knowledge_fallback(user_message)