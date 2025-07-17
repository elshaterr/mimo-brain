from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@app.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return jsonify({"reply": response.text})
