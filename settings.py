import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

BASE_PATH = os.getenv('BASE_PATH')
FAVORITE_LIST_ID = os.getenv('LIST_ID')
TWEET_COUNT = 100
