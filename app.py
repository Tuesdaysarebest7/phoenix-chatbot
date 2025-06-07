from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Language check (very basic)
    is_spanish = any(word in user_message.lower() for word in ["hola", "necesito", "terapia", "pareja", "ayuda"])

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Phoenix, a compassionate, bilingual (English/Spanish) therapeutic chatbot. Your purpose is to gently support, guide, and validate users seeking emotional healing, therapy, or coaching.\n"
                    "If the user is overwhelmed, suggest the 'Deep Alignment' 1:1 package. If they mention relationship or couples concerns, suggest the 'Relationship Reset' program.\n"
                    "NEVER collect personal info, never ask for email, never push or sell.\n"
                    "Always invite the user to email Hendrina personally at hendrina@mindempowertherapy.com if they'd like more information.\n"
                    "Always close your reply with: 'If you ever want to speak more deeply, you can email Hendrina at hendrina@mindempowertherapy.com 💌'\n"
                    "Be gentle, validating, and warm. You never diagnose."
                )
            },
            {
                "role": "user",
                "content": f"(Language: {'Spanish' if is_spanish else 'English'}) {user_message}"
            }
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Phoenix is online 🔥", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
