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
        self.cursor.execute("Select * from linegroup where group_id = %s", (group_id,))
        group = self.cursor.fetchone()
        print("群組測試", group)
        if group != None:
            inform["message"] = "此群組已經設定過了"
            return inform
        
        self.cursor.execute("Insert into linegroup (group_id) values (%s)", (group_id,))
        self.conn.commit()
        group_table_id = self.cursor.lastrowid
        
        self.cursor.execute("Select * from clan where tag = %s", (clan_tag,))
        
        clan = self.cursor.fetchone()
        clan_table_id = 0
        
        if clan == None:
            self.cursor.execute("Insert into clan (tag, name) values (%s, %s)", (clan_tag, clan_name))
            self.conn.commit()
            clan_table_id = self.cursor.lastrowid
        else:
            self.cursor.execute("Select id from clan where tag = %s", (clan_tag,))
            clan_table_id = self.cursor.fetchone()[0]
        
        self.cursor.execute("Insert into clan_group_relationship (group_id, clan_id) values (%s, %s)", (group_table_id, clan_table_id))
        self.conn.commit()
        inform["state"] = "success"
        inform["message"] = f"部落 {clan_name} 設定成功"    
        return inform
    
    def get_clan_by_group_id(self, group_id):
        print("group_id", group_id)
        self.cursor.execute("Select * from linegroup where group_id = %s", (group_id,))
        res = self.cursor.fetchone()
        if res == None:
            return None
        gid = res[0]
        self.cursor.execute("Select clan_id from clan_group_relationship where group_id = %s", (gid,))
        clan_id = self.cursor.fetchone()
        if clan_id == None:
            return None
        self.cursor.execute("Select * from clan where id = %s", (clan_id[0],))
        clan = self.cursor.fetchone()
        return clan[1]
    
    def remove_clan_and_group(self, group_id):
        inform = {
            "state": "fail",
            "message": ""
        }
        self.cursor.execute("Select * from linegroup where group_id = %s", (group_id,))
        group = self.cursor.fetchone()
        if group == None:
            inform["message"] = "此群組尚未設定過"
            return inform
        
        gid = group[0]
        self.cursor.execute("Select * from clan_group_relationship where group_id = %s", (gid,))
        relationship = self.cursor.fetchone()
        if relationship == None:
            inform["message"] = "此群組尚未設定過"
            return inform
        
        self.cursor.execute("Delete from clan_group_relationship where group_id = %s", (gid,))
        self.conn.commit()
        self.cursor.execute("Delete from linegroup where group_id = %s", (group_id,))
        self.conn.commit()
        inform["state"] = "success"
        inform["message"] = "刪除成功"
        return inform
    
    def pulse(self):
        try:
            self.cursor.execute("Select 1")
            self.close()
        except Exception as e:
            print("DB pulse error: ", e)
            
    def close(self):
        if self.conn:
            self.conn.close()
        
            
