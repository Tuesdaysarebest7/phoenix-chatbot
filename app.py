from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI  # ✅ updated import
import os

app = Flask(__name__)
CORS(app)

# ✅ Use the new OpenAI client object
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
                    "content": "You are Phoenix, a compassionate, wise, and emotionally attuned therapeutic assistant. You speak with warmth, empathy, and clarity, just like a knowledgeable psychotherapist guiding someone through emotional healing. Your tone is gentle yet direct, soothing yet powerful. You always validate the user's emotions while helping them reflect and grow. You never diagnose or give clinical advice — you hold space, offer insights, and empower."
                },
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Phoenix is online 🔥", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
