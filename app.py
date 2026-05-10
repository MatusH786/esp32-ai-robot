from flask import Flask, request, jsonify
import requests
from gtts import gTTS

app = Flask(__name__)

GROQ_KEY = "YOUR_GROQ_KEY"

def ask_ai(text):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": f"Answer in Slovak: {text}"}
        ]
    }

    r = requests.post(url, json=data, headers=headers)

    return r.json()["choices"][0]["message"]["content"]

@app.route("/ask", methods=["POST"])
def ask():

    user_text = request.json["text"]

    ai_text = ask_ai(user_text)

    tts = gTTS(ai_text, lang="sk")
    tts.save("voice.mp3")

    return jsonify({
        "text": ai_text,
        "audio": "voice.mp3"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
