from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyBN4HDN3tAsC3NPayscGEXwDEkSVtumarY"

@app.route("/api/mimo", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "برجاء إدخال رسالة."})

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_message}]}]}

    response = requests.post(
        url + f"?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"response": reply})
    else:
        return jsonify({"response": "حدث خطأ أثناء الاتصال بـ Gemini."})

if __name__ == "__main__":
    app.run()
