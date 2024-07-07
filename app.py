from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
logging.debug(f"OpenAI API Key Loaded: {openai.api_key}")

# Define the Assistant ID from the screenshot
ASSISTANT_ID = "asst_rONRVfEEL2eup5TGf71WEyYK"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    logging.debug(f"User Message: {user_message}")
    
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

@app.route('/useTrigramAgents', methods=['POST'])
def use_trigram_agents():
    query = request.json['query']
    logging.debug(f"Query: {query}")
    
    # Making a call to the agent API (this should be updated with the actual endpoint and structure)
    try:
        agent_response = openai.Function.call(
            assistant_id=ASSISTANT_ID,
            function_name="useTrigramAgents",
            parameters={"mainQuery": query}
        )
        
        if agent_response:
            logging.debug(f"Agent Response: {agent_response}")
            return jsonify(agent_response)
        else:
            logging.error("Agent API call failed")
            return jsonify({"message": "I apologize, but the agent API call failed."})
    except Exception as e:
        logging.error(f"Error during agent API call: {e}")
        return jsonify({"message": "An error occurred during the agent API call."})

if __name__ == "__main__":
    app.run(debug=True)