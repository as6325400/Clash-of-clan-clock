import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys

load_dotenv()

class Clan():
    def __init__(self, tag):
        self.base_request_url = f"{os.getenv('REQUEST_URL')}clans/"
        self.tag = "%23" + tag[1:]
        self.headers = {
            "Accept": "application/json",
            "authorization": f"Bearer {os.getenv('CLASHOFCLAN_TOKEN')}"
        }
    
    def clan_exist(self):
        url = f"{self.base_request_url}{self.tag}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                return True
            else:
                return False
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            
    def clan_capital_not_end(self):
        url = f"{self.base_request_url}{self.tag}/capitalraidseasons"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                data = response.json()
                data = data["items"][0]
                
                if data["state"] != "ongoing":
                    return {
                        "state": data["state"]
                    }
                
                inform = {
                    "state": data["state"],
                    "attack_member_nums": len(data["members"]),
                    "member_list": []
                }
                
                for member in data['members']:
                    inform["member_list"].append({
                        "name": member["name"],
                        "tag": member["tag"],
                        "attack_times": int(member["attacks"]),
                        "total_attack_nums": int(member["attackLimit"]) + int(member["bonusAttackLimit"])
                    })
                return inform
            
            else:
                return None
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            
    def clan_memberlist(self):
        url = f"{self.base_request_url}{self.tag}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                data = response.json()
                member_list = []
                for member in data["memberList"]:
                    member_list.append({
                        "name": member["name"],
                        "tag": member["tag"],
                    })
                return member_list
            else:
                return None
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            
    def clan_capital_not_start(self):
        url = f"{self.base_request_url}{self.tag}/capitalraidseasons"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                data = response.json()
                data = data["items"][0]
                
                if data["state"] != "ongoing":
                    return {
                        "state": data["state"]
                    }
                
                inform = {
                    "state": data["state"],
                    "attack_member_nums": len(data["members"]),
                    "member_list": []
                }
                
                clan_member_list = self.clan_memberlist()
                for member in clan_member_list:
                    if member["tag"] not in [i["tag"] for i in data["members"]]:
                        inform["member_list"].append({
                            "name": member["name"],
                            "tag": member["tag"],
                        })
                return inform
            
            else:
                return None
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
    
    def clan_war_not_end(self):
        url = f"{self.base_request_url}{self.tag}/currentwar"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                data = response.json()
                
                inform = {
                    "state": data["state"],
                    "member_list": []
                }
                
                if data["state"] != "inWar":
                    return inform
                
                for member in data['clan']['members']:
                    if member.get("attacks"):
                        
                        if len(member["attacks"]) >= 2:
                            continue
                        
                        inform["member_list"].append({
                            "name": member["name"],
                            "tag": member["tag"],
                            "attack_times": int(len(member["attacks"])),
                        })
                        
                    else:
                        inform["member_list"].append({
                            "name": member["name"],
                            "tag": member["tag"],
                            "attack_times": 0,
                        })
                return inform
            
            else:
                return None
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
    
            
    