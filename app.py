from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a global assistant object
assistant = openai.beta.assistants.create(
    name="Sopheon",
    instructions="You are Sopheon, a wise and empathetic AI assistant. Provide thoughtful and helpful responses.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # Create a new thread for each conversation
    thread = openai.beta.threads.create()

    # Add the user's message to the thread
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Run the assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Wait for the run to complete
    while run.status != "completed":
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Retrieve the assistant's messages
    messages = openai.beta.threads.messages.list(thread_id=thread.id)

    # Get the last message from the assistant
    assistant_message = next((msg for msg in messages if msg.role == "assistant"), None)

    if assistant_message:
        return jsonify({"message": assistant_message.content[0].text.value})
    else:
        return jsonify({"message": "I apologize, but I couldn't generate a response."})

if __name__ == "__main__":
    app.run(debug=True)