import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    GPT40_API_URL = os.getenv('GPT40_API_URL')
    GPT40_API_KEY = os.getenv('GPT40_API_KEY')
    NOTION_CLIENT_ID = os.getenv('NOTION_CLIENT_ID')
    NOTION_CLIENT_SECRET = os.getenv('NOTION_CLIENT_SECRET')
    NOTION_REDIRECT_URI = os.getenv('NOTION_REDIRECT_URI')
    MONGO_URI = os.getenv('MONGO_URI')