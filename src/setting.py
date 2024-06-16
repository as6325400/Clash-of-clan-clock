import os
from dotenv import load_dotenv

load_dotenv()

content = """
若要綁定此 line 群組與部落，請輸入以下指令：
/clock <部落標籤>

例如：
/clock #9LY9RLRL


若要解除綁定，請輸入以下指令：
/clock -r
"""

github_link = os.getenv("GITHUB_LINK")
google_form_link = os.getenv("GOOGLE_FORM_LINK")
introduce = f"""
在聊天室裡單獨輸入一個 clock 指令，可開啟此機器人的功能選單。

須先設定部落標籤，才能使用此機器人。
設定方法請點擊「設定教學」。
機器人將會自動發送設定教學。

若要查看正在進行的部落戰，請點擊「部落戰」。
會顯示部落戰的剩餘時間及時間相關資訊
會顯示所有未將兩場部落戰打完的成員 ID

若要查看首都突襲補刀，請點擊 「突襲尚未完成名單」。
會顯示當前整個部落參與突襲的人員數量
以及顯示未將六場突襲打完的成員 ID

若要查看尚未參與首都突襲的成員，請點擊 「突襲尚未參與名單」。
會顯示當前在部落中，且未參與此部落突襲的成員 ID

關於此專案：

此為專案的 github 連結：
{github_link}

若方便的話希望大家幫我按個 star，謝謝！

若有出現問題 bug 或建議，可以填寫此回饋表單：
{google_form_link}
"""