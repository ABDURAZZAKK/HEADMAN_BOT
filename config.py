import os 
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
PROXY_TOKEN = os.getenv("PROXY_TOKEN")
PROXY_PROTOCOL = os.getenv("PROXY_PROTOCOL")
MY_ID = int(os.getenv("MY_ID"))

