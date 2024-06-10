import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys

load_dotenv()

class Clan():
    def __init__(self, tag):
        self.base_request_url = f"{os.getenv('REQUEST_URL')}clans/"
        self.tag = tag
    
    def clan_exist(self):
        url = f"{self.base_request_url}%23{self.tag[1:]}"
        headers = {
            "Accept": "application/json",
            "authorization": f"Bearer {os.getenv('CLASHOFCLAN_TOKEN')}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if(response.status_code == 200):
                return True
            else:
                return False
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            
    
            
    