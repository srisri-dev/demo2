import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Create a .env file and add your Gemini API key.")

client = genai.Client(api_key=api_key)

# Requested Gemini model
MODEL_NAME = "gemini-3.6-flash"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser question:\n{user_message}"
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return jsonify({"reply": response.text or "I couldn't generate a response."})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
