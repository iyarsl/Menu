import os

from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import errors

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# Tried in order; falls through to the next if a model is overloaded (503).
MODELS = ["gemini-3.5-flash", "gemini-2.5-flash"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not client:
        return jsonify({"error": "GEMINI_API_KEY environment variable is not set."}), 500

    prompt = request.json.get("prompt", "")

    last_error = None
    for model in MODELS:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            return jsonify({"response": response.text})
        except errors.ServerError as e:
            last_error = e

    return jsonify({"error": str(last_error)}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
