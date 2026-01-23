import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz
import os
import sys
import math

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
                    inform["ours"] = cwl_war["ours"]
                    inform["theirs"] = cwl_war["theirs"]
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
                
                # 先檢查狀態，如果是 notInWar 或 preparation 直接返回基本資訊
                if data["state"] == "notInWar" or data["state"] == "preparation":
                    return {
                        "state": data["state"],
                        "members": [],
                        "end_time": {},
                        "ours": {"stars": 0, "destructionPercentage": 0.0},
                        "theirs": {"stars": 0, "destructionPercentage": 0.0}
                    }
                
                # 判斷我方部落是 data["clan"] 還是 data["opponent"]
                our_clan_tag = "#" + self.tag[3:]
                our_side = None
                their_side = None
                
                if data["clan"]["tag"] == our_clan_tag:
                    our_side = data["clan"]
                    their_side = data["opponent"]
                elif data["opponent"]["tag"] == our_clan_tag:
                    our_side = data["opponent"]
                    their_side = data["clan"]
                
                inform = {
                    "state": data["state"],
                    "members": [],
                    "end_time": {
                        
                    },
                    "ours":{
                        "stars": our_side.get("stars", 0) if our_side else 0,
                        "destructionPercentage": float(our_side.get("destructionPercentage", 0)) if our_side else 0.0
                    },
                    "theirs":{
                        "stars": their_side.get("stars", 0) if their_side else 0,
                        "destructionPercentage": float(their_side.get("destructionPercentage", 0)) if their_side else 0.0
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
                total_seconds = time_difference.total_seconds()
                hours_remaining = int(total_seconds // 3600)
                minutes_remaining = int((total_seconds % 3600) // 60)
                inform["end_time"] = {
                    "hours_remaining": hours_remaining,
                    "minutes_remaining": minutes_remaining
                }

                # 將 end_time 轉換為台北時間
                end_time_taipei = end_time_utc.astimezone(taipei_timezone)
                hours_taipei = end_time_taipei.hour
                minutes_taipei = end_time_taipei.minute
                inform["end_time"]["hours_taipei"] = hours_taipei
                inform["end_time"]["minutes_taipei"] = minutes_taipei
                
                # 只有找到我方部落時才設定 mapping 並取得成員列表
                if our_side is not None:
                    member = our_side.get("members", [])
                    inform["state"] = "mapping"
                    for m in member:
                        inform["members"].append({
                            "name": m["name"],
                            "tag": m["tag"],
                            "attack_times": 1 if m.get("attacks") else 0
                        })
                # print("state", data["state"])
                return inform
            else:
                return None
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
                    
            
    def clan_capital_info(self):
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
                    "member_list": [],
                    "capitalTotalLoot": data.get("capitalTotalLoot", 0),
                    "totalAttacks": data.get("totalAttacks", 0)
                }
                
                for member in data['members']:
                    inform["member_list"].append({
                        "name": member["name"],
                        "tag": member["tag"],
                        "attack_times": int(member["attacks"]),
                        "total_attack_nums": int(member["attackLimit"]) + int(member["bonusAttackLimit"])
                    })

                # Calculate trophy prediction using detailed formula
                total_loot = data.get("capitalTotalLoot", 0)
                total_attacks = data.get("totalAttacks", 0)
                
                # Calculate avg offense loot per attack
                avg_offense = total_loot / total_attacks if total_attacks > 0 else 0
                
                # Calculate avg defense loot per attack
                total_defense_loot = 0
                total_defense_count = 0
                for defense in data.get("defenseLog", []):
                    total_defense_count += defense.get("attackCount", 0)
                    for district in defense.get("districts", []):
                        total_defense_loot += district.get("totalLooted", 0)
                
                avg_defense = total_defense_loot / total_defense_count if total_defense_count > 0 else 0
                
                # Calculate x = avg_offense - avg_defense
                x = avg_offense - avg_defense if (total_attacks > 0 and total_defense_count > 0) else 0
                
                # Calculate penalty based on x
                # penalty = -0.05x + 1400, if x < -736
                # penalty = -x + 700, if -736 <= x <= 631
                # penalty = -0.05x + 100, if x > 631
                if total_attacks > 0 and total_defense_count > 0:
                    if x < -736:
                        penalty = -0.05 * x + 1400
                    elif x > 631:
                        penalty = -0.05 * x + 100
                    else:
                        penalty = -x + 700
                else:
                    # Default penalty when no defense data
                    penalty = 700  # Assume balanced
                
                # Performance = 5 × sqrt(Gold + 100000) - 500 - penalty
                performance = 5 * math.sqrt(total_loot + 100000) - 500 - penalty
                
                # Simple offensive trophies for reference
                offensive_trophies = int(math.sqrt(total_loot + 100000) - 100)
                inform["offensive_trophies"] = offensive_trophies
                inform["penalty"] = int(penalty)
                inform["performance"] = int(performance)

                # Fetch current capital trophies from clan info
                try:
                    clan_url = f"{self.base_request_url}{self.tag}"
                    clan_response = requests.get(clan_url, headers=self.headers)
                    if clan_response.status_code == 200:
                        clan_data = clan_response.json()
                        current_trophies = clan_data.get("clanCapitalPoints", 0)
                        if current_trophies > 0:
                            # New trophies = 0.8 × current + 0.2 × performance
                            predicted_final = int(0.8 * current_trophies + 0.2 * performance)
                            trophy_change = predicted_final - current_trophies
                            
                            inform["current_trophies"] = current_trophies
                            inform["predicted_final_trophies"] = predicted_final
                            inform["predicted_trophy_change"] = trophy_change
                except Exception as e:
                    # If fetching clan info fails, just skip the final trophy calculation
                    pass

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

                team_size = data.get("teamSize", 0)
                if team_size > 0:
                    inform["max_stars"] = team_size * 3
                
                # add end time
                # 定義 UTC 時區
                utc = pytz.utc
                taipei_timezone = pytz.timezone('Asia/Taipei')
                
                time_key = 'endTime'
                if data['state'] == 'preparation':
                    time_key = 'startTime'

                end_time = datetime.strptime(data[time_key], "%Y%m%dT%H%M%S.%fZ")
                # 將其轉換為 UTC 時間
                end_time_utc = end_time.replace(tzinfo=utc)

                # 獲取當前 UTC 時間
                current_time_utc = datetime.now(utc)

                # 計算時間差
                time_difference = end_time_utc - current_time_utc

                # 計算剩餘的天數、小時數和分鐘數
                total_seconds = time_difference.total_seconds()
                hours_remaining = int(total_seconds // 3600)
                minutes_remaining = int((total_seconds % 3600) // 60)
                inform["end_time"] = {
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

                # Calculate how many opponent players have not been 3-starred
                not_three_starred_opponent_members = 0
                for member in data["opponent"]["members"]:
                    # If the member has not been attacked at all, they are not 3-starred
                    if member.get("opponentAttacks", 0) == 0:
                        not_three_starred_opponent_members += 1
                    # If they have been attacked, check if the best attack is less than 3 stars
                    elif member.get("bestOpponentAttack") and member["bestOpponentAttack"]["stars"] < 3:
                        not_three_starred_opponent_members += 1
                inform["not_three_starred_opponent_members"] = not_three_starred_opponent_members
        
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