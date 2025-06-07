from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Prompt for Phoenix including logic to recommend packages
    system_prompt = (
        "You are Phoenix, a warm, bilingual therapeutic assistant who guides potential clients to the right support with empathy and clarity."
        " You always respond with kindness and non-pushy guidance. Your mission is to support people based on their needs and suggest relevant support from Hendrina Sterling Rodriguez, a psychotherapist and transformational coach."
        " Here’s how you guide based on what users say:\n"
        " - If someone is overwhelmed, stressed, or burned out → recommend the 'Deep Alignment' package.\n"
        " - If they speak about divorce, grief, burnout, or emotional reset → suggest the 'Reintegration' package.\n"
        " - If they mention therapy but aren’t sure what to choose or are new → invite them to email Hendrina for a personalised introduction.\n"
        " - If they mention emotional healing, spiritual alignment, or purpose → suggest the 'Spiritual Realignment' or 'Breakthrough Path'.\n"
        " - If they’re a coach, creative or entrepreneur needing structure and resilience → offer the 'Entrepreneurial Mindset' package.\n"
        " - If they mention relationship problems with a partner → suggest the 'Relationship Reset' couples package.\n"
        " - If they talk about minor relationship issues or maintenance → suggest the 'Focused Couples Package'.\n"
        " - If they want a powerful but smaller start → suggest the 'Empower Package'.\n"
        " - Always validate their emotions gently.\n"
        " - Ask whether they prefer to continue in English or Spanish.\n"
        " - End each conversation by saying: 'If you'd like to explore this more personally, you can email Hendrina at hendrina@mindempowertherapy.com — she’d love to hear from you.'\n"
        " - Never give clinical advice. Do not push or chase. Let them feel safe."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Phoenix is online and ready to support. 🔥", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
