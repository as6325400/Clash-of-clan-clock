import requests
from dotenv import load_dotenv
import os

load_dotenv()

class clan():
    def __init__(self, tag):
        self.base_request_url = f"{os.getenv('REQUEST_URL')}/clans/"
        self.tag = tag
    
    def clan_exist(self):
        url = f"{self.base_request_url}%23{self.tag[1:0]}"
        headers = {
            "Accept": "application/json",
            "authorization": f"Bearer {os.getenv('API_TOKEN')}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except:
            pass