import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

class DB():
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("ALEMBIC_HOST"),
            user=os.getenv("ALEMBIC_USER"),
            password=os.getenv("ALEMBIC_PASSWORD"),
            database=os.getenv("ALEMBIC_DB"),
            port=int(os.getenv("ALEMBIC_PORT")),
        )
        self.cursor = self.conn.cursor()
    
    def add_clan_and_group(self, clan_tag, clan_name, group_id):
        inform = {
            "state": "fail",
            "message": ""
        }
        self.cursor.execute(f"Select * from linegroup where group_id = '{group_id}'")
        group = self.cursor.fetchone()
        print("群組測試", group)
        if group != None:
            inform["message"] = "此群組已經設定過了"
            return inform
        
        self.cursor.execute(f"Insert into linegroup (group_id) values ('{group_id}')")
        self.conn.commit()
        group_table_id = self.cursor.lastrowid
        
        self.cursor.execute(f"Select * from clan where tag = '{clan_tag}'")
        
        clan = self.cursor.fetchone()
        clan_table_id = 0
        
        if clan == None:
            self.cursor.execute(f"Insert into clan (tag, name) values ('{clan_tag}', '{clan_name}')")
            self.conn.commit()
            clan_table_id = self.cursor.lastrowid
        else:
            self.cursor.execute(f"Select id from clan where tag = '{clan_tag}'")
            clan_table_id = self.cursor.fetchone()[0]
        
        self.cursor.execute(f"Insert into clan_group_relationship (group_id, clan_id) values ('{group_table_id}', '{clan_table_id}')")
        self.conn.commit()
        inform["state"] = "success"
        inform["message"] = f"部落 {clan_name} 設定成功"    
        return inform
    
    def get_clan_by_group_id(self, group_id):
        print("group_id", group_id)
        self.cursor.execute(f"Select * from linegroup where group_id = '{group_id}'")
        res = self.cursor.fetchone()
        if res == None:
            return None
        gid = res[0]
        self.cursor.execute(f"Select clan_id from clan_group_relationship where group_id = '{gid}'")
        clan_id = self.cursor.fetchone()
        if clan_id == None:
            return None
        self.cursor.execute(f"Select * from clan where id = '{clan_id[0]}'")
        clan = self.cursor.fetchone()
        return clan[1]
    
    def remove_clan_and_group(self, group_id):
        inform = {
            "state": "fail",
            "message": ""
        }
        self.cursor.execute(f"Select * from linegroup where group_id = '{group_id}'")
        group = self.cursor.fetchone()
        if group == None:
            inform["message"] = "此群組尚未設定過"
            return inform
        
        gid = group[0]
        self.cursor.execute(f"Select * from clan_group_relationship where group_id = '{gid}'")
        relationship = self.cursor.fetchone()
        if relationship == None:
            inform["message"] = "此群組尚未設定過"
            return inform
        
        self.cursor.execute(f"Delete from clan_group_relationship where group_id = '{gid}'")
        self.conn.commit()
        self.cursor.execute(f"Delete from linegroup where group_id = '{group_id}'")
        self.conn.commit()
        inform["state"] = "success"
        inform["message"] = "刪除成功"
        return inform
    
    def close(self):
        if self.conn:
            self.conn.close()
        
            