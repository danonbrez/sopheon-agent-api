# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/useTrigramAgents', methods=['POST'])
def use_trigram_agents():
    data = request.json
    main_query = data.get('mainQuery')

    # Simulate agent processing
    responses = [
        {"agentName": "Agent1_Heaven", "response": "Overall strategy for " + main_query},
        {"agentName": "Agent2_Lake", "response": "Positive impacts of " + main_query},
        {"agentName": "Agent3_Fire", "response": "Clarity on " + main_query},
        {"agentName": "Agent4_Thunder", "response": "Urgent actions for " + main_query},
        {"agentName": "Agent5_Wind", "response": "Holistic considerations for " + main_query},
        {"agentName": "Agent6_Water", "response": "Complexities in " + main_query},
        {"agentName": "Agent7_Mountain", "response": "Fundamental principles for " + main_query},
        {"agentName": "Agent8_Earth", "response": "Adaptability for " + main_query},
    ]

    final_response = "Combined response for " + main_query
    return jsonify({"finalResponse": final_response, "individualResponses": responses})

if __name__ == '__main__':
    app.run(debug=True)