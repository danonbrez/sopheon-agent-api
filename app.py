from flask import Flask, render_template, request, jsonify, Response
from flask_sse import sse
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import certifi
import time  # To simulate real-time typing

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
logging.basicConfig(level=logging.DEBUG)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the Assistant ID
ASSISTANT_ID = "asst_r0NRV1EEL2eup5TGf71WEyYK"

# Ensure Certifi is used for SSL certificate verification
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    logging.debug(f"User Message: {user_message}")

    def generate_response():
        # Simulate real-time typing with a typing indicator
        yield "data: typing\n\n"
        
        try:
            # Create a new thread for this conversation
            thread = client.beta.threads.create()

            # Add the user's message to the thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )

            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID,
                model="gpt-4-turbo"
            )

            # Wait for the run to complete
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                time.sleep(1)

            # Retrieve the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_message = messages.data[0].content[0].text.value

            # Simulate typing out the response
            for char in assistant_message:
                yield f"data: {char}\n\n"
                time.sleep(0.05)  # Adjust speed of typing here

        except Exception as e:
            logging.error(f"Error in chat endpoint: {str(e)}")
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate_response(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)