import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
from config import Config

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLS)

def call_gpt40_api(task):
    headers = {
        "Authorization": f"Bearer {Config.GPT40_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": task}
    session = requests.Session()
    session.mount("https://", SSLAdapter())
    try:
        response = session.post(Config.GPT40_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.SSLError as e:
        return {"error": "SSL error occurred", "details": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": "Request error occurred", "details": str(e)}