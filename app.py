from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Define the payload for GPT-4 API
    response = openai.Completion.create(
        model="gpt-4",
        prompt=user_message,
        max_tokens=50,
        temperature=0.7
    )
    
    if response:
        assistant_message = response.choices[0].text.strip()
        return jsonify({"message": assistant_message})
    else:
        return jsonify({"message": "I apologize, but I couldn't generate a response."})

if __name__ == "__main__":
    app.run(debug=True)