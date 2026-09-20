"""
Broski AI Assistant - backend

Run:
    pip install -r requirements.txt
    copy .env.example to .env and put your key in it
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import datetime

from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("BROSKI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY) if API_KEY else None

app = Flask(__name__, static_folder="static", static_url_path="/static")

SYSTEM_PROMPT = (
    "You are Broski, a friendly voice assistant. "
    "Answer in at most three short spoken-style sentences. "
    "No markdown, no bullet lists, no emoji - your words are read aloud."
)

# Sites the assistant knows how to open. The browser does the opening;
# the backend just decides which URL to send back.
SITES = {
    "youtube": "https://www.youtube.com",
    "wikipedia": "https://www.wikipedia.org",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
}


def local_command(text):
    """Handle the things that need no AI. Returns a dict or None."""
    t = text.lower().strip()

    for name, url in SITES.items():
        if f"open {name}" in t:
            return {"reply": f"Opening {name}.", "open_url": url}

    if "time" in t:
        return {"reply": "The time is " + datetime.datetime.now().strftime("%I:%M %p")}

    if "date" in t or "what day" in t:
        return {"reply": "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y")}

    if "your name" in t or "who are you" in t:
        return {"reply": "I am Broski, your AI assistant."}

    return None


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    # history is a list of {"role": "user"|"assistant", "content": "..."}
    history = data.get("history") or []

    if not message:
        return jsonify({"reply": "I didn't catch that. Say it again?"})

    handled = local_command(message)
    if handled:
        return jsonify(handled)

    if client is None:
        return jsonify({
            "reply": "No API key is set, so I can only do time, date and opening sites."
        })

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # keep the last 10 turns so the conversation stays cheap
    messages += history[-10:]
    messages.append({"role": "user", "content": message})

    try:
        result = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        return jsonify({"reply": result.choices[0].message.content.strip()})
    except Exception as exc:
        app.logger.exception("model call failed")
        return jsonify({"reply": "My connection to the model failed.",
                        "error": str(exc)}), 502


if __name__ == "__main__":
    if client is None:
        print("! OPENAI_API_KEY is not set - built-in commands only.")
    app.run(debug=True, port=5000)
