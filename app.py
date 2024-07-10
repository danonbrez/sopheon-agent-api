from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import logging
import certifi

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the Assistant ID
ASSISTANT_ID = "asst_r0NRV1EEL2eup5TGf71WEyYK"

# Ensure Certifi is used for SSL certificate verification
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Global variable to store thread ID
thread_id = None

@app.route('/')
def index():
    return render_template('index.html')

def start_new_thread():
    global thread_id
    response = openai.Completion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    )
    thread_id = response['id']

def add_message_to_thread(role, content):
    global thread_id
    if thread_id is None:
        start_new_thread()

    openai.Completion.create(
        model="gpt-4",
        messages=[
            {"role": role, "content": content}
        ],
        thread_id=thread_id
    )

def get_assistant_response():
    global thread_id
    response = openai.Completion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Generate response based on the previous messages."}
        ],
        thread_id=thread_id
    )
    assistant_message = response.choices[0].message['content']
    return assistant_message

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    logging.debug(f"User Message: {user_message}")

    try:
        # Add user message to thread
        add_message_to_thread('user', user_message)

        # Get assistant's response
        assistant_message = get_assistant_response()
        logging.debug(f"Assistant Message: {assistant_message}")
        
        return jsonify({"message": assistant_message})

    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)