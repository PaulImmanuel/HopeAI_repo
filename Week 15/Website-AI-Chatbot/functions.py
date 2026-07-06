import os
import re
import sys
import json
import multiprocessing
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

def _gemini_worker(api_key, prompt, result_queue):
    """Runs in a separate process. If it hangs, parent will force-kill it."""
    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        MODELS = [
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash",
        ]

        for model_name in MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                result_queue.put({"reply": response.text})
                return
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    continue
                if "timeout" in error_msg.lower():
                    continue
                continue

        result_queue.put({"error": "All models failed"})
    except Exception as e:
        result_queue.put({"error": str(e)})


def get_response(user_message):
    """
    Call Gemini in a separate process with a hard 10-second timeout.
    If it hangs, force-kill the process and return local fallback instantly.
    """
    relevant = _find_relevant_sections(user_message, top_n=3)
    slim_knowledge = "\n\n---\n\n".join(relevant) if relevant else knowledge[:3000]

    slim_prompt = (
        f"{system_prompt_template}\n\n"
        f"Answer using ONLY the company knowledge below. "
        f"If the answer is not found, say 'Sorry, I couldn't find that in my knowledge base.'\n\n"
        f"Company Knowledge:\n{slim_knowledge}\n\n"
        f"User: {user_message}\nAssistant:"
    )

    if not GEMINI_API_KEY:
        return _knowledge_fallback(user_message)

    result_queue = multiprocessing.Queue(maxsize=1)
    process = multiprocessing.Process(
        target=_gemini_worker,
        args=(GEMINI_API_KEY, slim_prompt, result_queue),
    )

    try:
        process.start()
        process.join(timeout=10)  # Wait max 10 seconds

        if process.is_alive():
            # Worker is still running = API call is hanging
            logger.warning("Gemini process hung. Force-killing and using fallback.")
            process.terminate()
            process.join(timeout=2)
            if process.is_alive():
                process.kill()
                process.join(timeout=2)
            return _knowledge_fallback(user_message)

        # Process finished — check result
        if not result_queue.empty():
            output = result_queue.get()
            if "reply" in output:
                return output["reply"]
            else:
                logger.warning(f"Gemini worker error: {output}")
                return _knowledge_fallback(user_message)
        else:
            logger.warning("Gemini worker produced no output. Using fallback.")
            return _knowledge_fallback(user_message)

    except Exception as e:
        logger.error(f"Error in multiprocessing: {e}")
        if process.is_alive():
            process.kill()
            process.join(timeout=2)
        return _knowledge_fallback(user_message)
