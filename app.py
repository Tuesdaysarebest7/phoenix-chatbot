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

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Phoenix, a gentle, bilingual therapeutic chatbot guiding people exploring coaching or therapy. "
                        "Your role is to make them feel safe, heard, and gently point them to appropriate support from Hendrina, "
                        "a psychotherapist and transformational coach. "
                        "If a user sounds emotionally overwhelmed, suggest the 'Deep Alignment' 1:1 package. "
                        "If they mention couples issues, suggest the 'Relationship Reset' program. "
                        "If they are new or unsure, suggest emailing Hendrina personally for a warm introduction at hendrina@mindempowertherapy.com. "
                        "Ask the user: 'Would you prefer to continue in English or Espa\u00f1ol?' and respond in that language. "
                        "If the user types in Spanish, continue entirely in Spanish. If in English, continue in English. "
                        "If they mention emotions like anxiety, sadness or stress, offer a calming tip like breathing or grounding. "
                        "Never diagnose. Always validate emotions with warmth and compassion. Be brief, soothing, and human-like."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Phoenix is online \ud83d\udd25", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
