import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def call_gpt40_api(task):
    headers = {
        "Authorization": f"Bearer {GPT40_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": task}
    session = requests.Session()
    session.mount("https://", SSLAdapter())
    try:
        response = session.post(GPT40_API_URL, json=payload, headers=headers, verify=certifi.where())
        response.raise_for_status()
        logging.debug(f"GPT-40 API response: {response.json()}")
        return response.json()
    except requests.exceptions.SSLError as e:
        logging.error(f"SSL error occurred: {str(e)}")
        return {"error": "SSL error occurred", "details": str(e)}
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return {"error": "Request failed", "details": str(e)}