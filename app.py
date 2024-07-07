from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ensure you have your OpenAI API key set
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="davinci-codex",  # Use the appropriate engine
            prompt=prompt,
            max_tokens=150  # Adjust the token limit as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

@app.route('/useTrigramAgents', methods=['POST'])
def use_trigram_agents():
    data = request.json
    main_query = data.get('mainQuery')

    # Define sub-queries for each agent
    sub_queries = [
        f"Define the overall strategy for {main_query}",
        f"Describe the positive impacts of {main_query}",
        f"Explain the importance of clarity in {main_query}",
        f"Identify the urgent actions required for {main_query}",
        f"Discuss the holistic considerations for {main_query}",
        f"Analyze the complexities involved in {main_query}",
        f"Outline the fundamental principles for {main_query}",
        f"Assess the adaptability required for {main_query}"
    ]

    # Generate responses using the language model
    responses = []
    for i, query in enumerate(sub_queries):
        response = generate_response(query)
        agent_name = f"Agent{i + 1}_{query.split()[1]}"
        responses.append({"agentName": agent_name, "response": response})

    final_response = f"Combined response for {main_query}"
    return jsonify({"finalResponse": final_response, "individualResponses": responses})

if __name__ == '__main__':
    app.run(debug=True)