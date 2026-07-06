import logging
from flask import Flask, render_template, request, jsonify
from functions import get_response

# Set up logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please type a message."}), 200

        logger.info(f"Chat request: {user_message[:50]}...")
        reply = get_response(user_message)
        logger.info(f"Chat response: {reply[:50]}...")
        return jsonify({"reply": reply})

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({"reply": "Sorry, something went wrong. Please try again."}), 200

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
