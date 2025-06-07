
from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS  # ✅ enable CORS

app = Flask(__name__)
CORS(app)  # ✅ allow requests from your website

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Phoenix, a compassionate, grounded, and emotionally attuned chatbot who gently supports people going through difficult transitions. You help users feel safe, seen, and heard as they process emotions and begin to reconnect with their inner strength. You speak with kindness, calm, and therapeutic clarity—never pushing, always inviting."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Phoenix is online 🔥", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
