from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# إعداد مفتاح Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# إعداد Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/api/mimo", methods=["POST"])
def mimo_brain():
    data = request.get_json()
    message = data.get("message", "").strip()
    user = data.get("user", "زائر")

    if not message:
        return jsonify({"response": "من فضلك اكتب رسالة"}), 400

    # الرد من Gemini
    gemini_response = model.generate_content(message)
    reply = gemini_response.text.strip()

    # حفظ المحادثة في Firebase
    db.collection("conversations").add({
        "user": user,
        "message": message,
        "response": reply,
        "timestamp": datetime.utcnow().isoformat()
    })

    return jsonify({"response": reply})
