from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import certifi

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management
logging.basicConfig(level=logging.DEBUG)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure Certifi is used for SSL certificate verification
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    logging.debug(f"User Message: {user_message}")

    if 'history' not in session:
        session['history'] = []

    session['history'].append({"role": "user", "content": user_message})

    try:
        response = client.Completion.create(
            model="gpt-4",
            messages=session['history']
        )

        assistant_message = response.choices[0].message.content.strip()
        logging.debug(f"Assistant Message: {assistant_message}")

        session['history'].append({"role": "assistant", "content": assistant_message})

        return jsonify({"message": assistant_message})

    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)