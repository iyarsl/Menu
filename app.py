import os

from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not client:
        return jsonify({"error": "GEMINI_API_KEY environment variable is not set."}), 500

    prompt = request.json.get("prompt", "")
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    return jsonify({"response": response.text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
