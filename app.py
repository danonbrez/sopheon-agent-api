from flask import Flask, request, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

NOTION_CLIENT_ID = os.getenv('NOTION_CLIENT_ID')
NOTION_CLIENT_SECRET = os.getenv('NOTION_CLIENT_SECRET')
NOTION_REDIRECT_URI = os.getenv('NOTION_REDIRECT_URI')

@app.route('/')
def index():
    return 'Welcome to Sopheon'

@app.route('/authorize')
def authorize():
    notion_authorize_url = (
        f"https://api.notion.com/v1/oauth/authorize?client_id={NOTION_CLIENT_ID}"
        f"&response_type=code&owner=user&redirect_uri={NOTION_REDIRECT_URI}"
    )
    return redirect(notion_authorize_url)

@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed', 400

    token_url = "https://api.notion.com/v1/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': NOTION_REDIRECT_URI,
        'client_id': NOTION_CLIENT_ID,
        'client_secret': NOTION_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        return 'Token exchange failed', 400

    token_json = response.json()
    access_token = token_json.get('access_token')

    # Store access_token securely in your database or session
    session['notion_access_token'] = access_token

    return 'Authorization successful'

if __name__ == '__main__':
    app.run(debug=True)