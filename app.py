import os
import logging
import time
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Initialize the OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the Assistant ID
ASSISTANT_ID = "asst_r0NRV1EEL2eup5TGf71WEyYK"  # Replace with your actual assistant ID

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    logging.debug(f"User Message: {user_message}")

    try:
        # Create a new thread
        thread = client.beta.threads.create()

        # Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            time.sleep(1)  # Wait for 1 second before checking again

        # Retrieve the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_message = next(
            (m.content[0].text.value for m in messages.data if m.role == "assistant"), None
        )
        
        if assistant_message is None:
            logging.error("Assistant did not respond.")
            return jsonify({"message": "Error: Assistant did not respond."})
    
        logging.debug(f"Assistant Message: {assistant_message}")
        return jsonify({"message": assistant_message})

    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"})

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)