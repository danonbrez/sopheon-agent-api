from flask import Flask, render_template, request, jsonify from openai import OpenAI from dotenv import load_dotenv import os import logging import certifiload_dotenv()  # Load environment variables from .env fileapp = Flask(name) logging.basicConfig(level=logging.DEBUG)Initialize the OpenAI clientclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))Define the Assistant IDASSISTANT_ID = "asst_r0NRV1EEL2eup5TGf71WEyYK"Ensure Certifi is used for SSL certificate verificationos.environ["REQUESTS_CA_BUNDLE"] = certifi.where()@app.route('/') def index(): return render_template('index.html')@app.route('/chat', methods=['POST']) def chat(): user_message = request.json['message'] logging.debug(f"User Message: {user_message}")try:
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
        model="gpt-4-turbo"  # Ensure correct model name
    )

    # Wait for the run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_message = messages.data[0].content[0].text.value

    logging.debug(f"Assistant Message: {assistant_message}")
    return jsonify({"message": assistant_message})

except Exception as e:
    logging.error(f"Error in chat endpoint: {str(e)}")
    return jsonify({"message": f"Error: {str(e)}"})@app.route('/useTrigramAgents', methods=['POST']) def use_trigram_agents(): query = request.json['query'] logging.debug(f"Received query for trigram agents: {query}") try: response = requests.post( "https://sopheon-agent-api-4cb6de5c7ca8.herokuapp.com/useTrigramAgents", json={"mainQuery": query}, headers={"Content-Type": "application/json"} ) if response.status_code == 200: agent_response = response.json() logging.debug(f"Agent Response: {agent_response}") return jsonify(agent_response) else: logging.error(f"Agent API call failed with status code {response.status_code} and response: {response.text}") return jsonify({"message": f"Agent API call failed with status code {response.status_code}", "details": response.text}) except Exception as e: logging.error(f"Error in useTrigramAgents endpoint: {str(e)}") return jsonify({"message": f"Error: {str(e)}"})if name == "main": app.run(debug=True)