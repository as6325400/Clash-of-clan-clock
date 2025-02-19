import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz
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
    
    def clan_info(self):
        url = f"{self.base_request_url}{self.tag}"
        inform = {
                "exist": False,
                "name": ""
            }
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if(response.status_code == 200):
                inform["exist"] = True
                inform["name"] = data["name"]
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}\n")
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            
        return inform
    
    def clan_cwl(self):
        url = f"{self.base_request_url}{self.tag}/currentwar/leaguegroup"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                data = response.json()
                inform = {
                    "state": data["state"],
                    "rounds": [],
                    "clans": [],
                    "member_list": []
                }
                
                if data["state"] == "notInWar" or data["state"] == "preparation":
                    return inform
                
                for round in data["rounds"]:
                    if round["warTags"][0] != "#0":
                        inform["rounds"].append(round["warTags"])
                
                cwl_war = self.catch_clan_cwl(inform["rounds"])
                if cwl_war != None:
                    # print("cwl_war", cwl_war)
                    inform["end_time"] = cwl_war["end_time"]
                    # inform["members"] = cwl_war["members"]
                    for member in cwl_war["members"]:
                        if member["attack_times"] == 0:
                            inform["member_list"].append(member)
                
                # print("inform", inform)
                return inform
            else:
                return None
            
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            
    def catch_clan_cwl(self, rounds):
        print("rounds", rounds)
        for round in rounds[::-1]:
            t = self.catch_clan_cwl_inform(round[0])
            if t == None or t["state"] == "notInWar" or t["state"] == "preparation":
                print("preparation", t["state"])
                continue
            elif t["state"] == "mapping" or t["state"] == "inWar":
                for tag in round[1:]:
                    if t != None and t["state"] == "mapping":
                        # print("t", t)
                        return t
                    t = self.catch_clan_cwl_inform(tag)
                return t
        return None
            
            
    def catch_clan_cwl_inform(self, tag):
        url = f"{self.base_request_url[:-6]}clanwarleagues/wars/{'%23' + tag[1:]}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if(response.status_code == 200):
                data = response.json()
                inform = {
                    "state": data["state"],
                    "members": [],
                    "end_time": {
                        
                    }
                }
                
                # add end time
                # 定義 UTC 時區
                utc = pytz.utc
                taipei_timezone = pytz.timezone('Asia/Taipei')
                end_time = datetime.strptime(data['endTime'], "%Y%m%dT%H%M%S.%fZ")
                # 將其轉換為 UTC 時間
                end_time_utc = end_time.replace(tzinfo=utc)

                # 獲取當前 UTC 時間
                current_time_utc = datetime.now(utc)

                # 計算時間差
                time_difference = end_time_utc - current_time_utc

                # 計算剩餘的天數、小時數和分鐘數
                days_remaining = time_difference.days
                seconds_remaining = time_difference.seconds
                hours_remaining, remainder = divmod(seconds_remaining, 3600)
                minutes_remaining, _ = divmod(remainder, 60)
                inform["end_time"] = {
                    "days_remaining": days_remaining,
                    "hours_remaining": hours_remaining,
                    "minutes_remaining": minutes_remaining
                }

                # 將 end_time 轉換為台北時間
                end_time_taipei = end_time_utc.astimezone(taipei_timezone)
                hours_taipei = end_time_taipei.hour
                minutes_taipei = end_time_taipei.minute
                inform["end_time"]["hours_taipei"] = hours_taipei
                inform["end_time"]["minutes_taipei"] = minutes_taipei
                
                # compare the final result
                
                member = None
                
                if data["state"] == "notInWar" or data["state"] == "preparation":
                    return inform
                
                if data["clan"]["tag"] == "#" + self.tag[3:]:
                    member = data["clan"]["members"]
                    
                elif data["opponent"]["tag"] == "#" + self.tag[3:]:
                    member = data["opponent"]["members"]
                    
                if member != None:
                    inform["state"] = "mapping"
                    for m in member:
                        inform["members"].append({
                            "name": m["name"],
                            "tag": m["tag"],
                            "attack_times": 1 if m.get("attacks") else 0
                        })
                        # print("m", m)
                # print("state", data["state"])
                return inform
            else:
                return None
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
                    "member_list": [],
                    "end_time": {
                        
                    },
                    "ours":{
                        "stars": data["clan"]["stars"],
                        "destructionPercentage": float(data["clan"]["destructionPercentage"])
                    },
                    "theirs":{
                        "stars": data["opponent"]["stars"],
                        "destructionPercentage": float(data["opponent"]["destructionPercentage"])
                    },
                    "final": 0
                }
                
                if data["state"] == "notInWar":
                    return inform
                
                # add end time
                # 定義 UTC 時區
                utc = pytz.utc
                taipei_timezone = pytz.timezone('Asia/Taipei')
                end_time = datetime.strptime(data['endTime'], "%Y%m%dT%H%M%S.%fZ")
                # 將其轉換為 UTC 時間
                end_time_utc = end_time.replace(tzinfo=utc)

                # 獲取當前 UTC 時間
                current_time_utc = datetime.now(utc)

                # 計算時間差
                time_difference = end_time_utc - current_time_utc

                # 計算剩餘的天數、小時數和分鐘數
                days_remaining = time_difference.days
                seconds_remaining = time_difference.seconds
                hours_remaining, remainder = divmod(seconds_remaining, 3600)
                minutes_remaining, _ = divmod(remainder, 60)
                inform["end_time"] = {
                    "days_remaining": days_remaining,
                    "hours_remaining": hours_remaining,
                    "minutes_remaining": minutes_remaining
                }

                # 將 end_time 轉換為台北時間
                end_time_taipei = end_time_utc.astimezone(taipei_timezone)
                hours_taipei = end_time_taipei.hour
                minutes_taipei = end_time_taipei.minute
                inform["end_time"]["hours_taipei"] = hours_taipei
                inform["end_time"]["minutes_taipei"] = minutes_taipei
                
                # compare the final result
                if inform["ours"]["stars"] > inform["theirs"]["stars"]:
                    inform["final"] = 1
                elif inform["ours"]["stars"] < inform["theirs"]["stars"]:
                    inform["final"] = -1
                else:
                    if inform["ours"]["destructionPercentage"] > inform["theirs"]["destructionPercentage"]:
                        inform["final"] = 1
                    elif inform["ours"]["destructionPercentage"] < inform["theirs"]["destructionPercentage"]:
                        inform["final"] = -1
                    else:
                        inform["final"] = 0
        
                if data["state"] != "inWar" and data["state"] != "warEnded" and data["state"] != "preparation":
                    return inform
                
                # add not war member
                try:
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
                except Exception as e:
                    print(f"An unexpected error occurred: {e}\n")
                    
                return inform
            
            else:
                return None
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
    
            
    