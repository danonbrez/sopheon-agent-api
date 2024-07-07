from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import logging
import requests
import certifi

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the Assistant ID from the screenshot
ASSISTANT_ID = "asst_rONRVfEEL2eup5TGf71WEyYK"

# Ensure Certifi is used for SSL certificate verification
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    logging.debug(f"User Message: {user_message}")
    
    # Define the payload for GPT-4 API using the chat/completions endpoint
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        if response:
            assistant_message = response['choices'][0]['message']['content'].strip()
            logging.debug(f"Assistant Message: {assistant_message}")
            return jsonify({"message": assistant_message})
        else:
            return jsonify({"message": "I apologize, but I couldn't generate a response."})
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/useTrigramAgents', methods=['POST'])
def use_trigram_agents():
    query = request.json['query']
    logging.debug(f"Received query for trigram agents: {query}")
    
    try:
        # Send the request to the trigram agent API
        response = requests.post(
            "https://sopheon-agent-api-4cb6de5c7ca8.herokuapp.com/useTrigramAgents",
            json={"mainQuery": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            agent_response = response.json()
            logging.debug(f"Agent Response: {agent_response}")
            return jsonify(agent_response)
        else:
            logging.error(f"Agent API call failed with status code {response.status_code} and response: {response.text}")
            return jsonify({"message": f"Agent API call failed with status code {response.status_code}", "details": response.text})
    except Exception as e:
        logging.error(f"Error in useTrigramAgents endpoint: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)