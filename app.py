import os
import sys
from argparse import ArgumentParser
from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, request, abort
from linebot.v3 import (
     WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent,
    JoinEvent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage
)


from linebot.models import FlexSendMessage, BubbleContainer

from dotenv import load_dotenv
from src import flex, setting
from model.clan import Clan
from model.db import DB

load_dotenv(override=True)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
port = os.getenv('PORT', 5000)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

@app.route("/")
def hello_world():
    print("hello world")
    return "app Start"

@app.route("/callback", methods=['POST'])
def callback():
    print("callback")
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(channel_secret)
        print(e)
        abort(400)
    except Exception as e:
        app.logger.error(f"Error handling webhook: {e}")
        abort(500)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        user_profile = line_bot_api.get_profile(event.source.user_id)
        if user_profile.user_id == line_bot_api.get_bot_info().user_id:
            app.logger.info("Message from bot itself, ignoring.")
            return
            
        flex_message = flex.flex_message
        if event.message.text.strip() == "clock":
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[FlexMessage.from_dict(flex_message)]
            ))
        else:
            argv = event.message.text.strip().split(" ")
            if argv[0] == "/clock":
                print(argv)
                if len(argv) == 2:
                    # add setting to db (group and clan tag)
                    if argv[1] != "-r":
                        print(event.source)
                        id = None
                        if event.source.type == "group":
                            id = event.source.group_id
                        elif event.source.type == "user":
                            id = event.source.user_id
                        clan_tag = argv[1]
                        clan = Clan(clan_tag)
                        inform = clan.clan_info()
                        if "exist" in inform and inform["exist"]:
                            db = DB()
                            res = db.add_clan_and_group(clan_tag, inform["name"], id)
                            db.close()
                            line_bot_api.reply_message(ReplyMessageRequest(
                                reply_token = event.reply_token, 
                                messages=[TextMessage(text=res["message"])]
                            ))
                        else:
                            print("clan not exist")
                            line_bot_api.reply_message(ReplyMessageRequest(
                                reply_token = event.reply_token, 
                                messages=[TextMessage(text=f"部落不存在或權限尚未開啟")]
                            ))
                    else:
                        # remove setting from db
                        id = None
                        if event.source.type == "group":
                            id = event.source.group_id
                        elif event.source.type == "user":
                            id = event.source.user_id
                        db = DB()
                        res = db.remove_clan_and_group(id)
                        db.close()
                        line_bot_api.reply_message(ReplyMessageRequest(
                            reply_token = event.reply_token, 
                            messages=[TextMessage(text=res["message"])]
                        ))
    return 'OK'

        
@handler.add(PostbackEvent)
def handle_message(event: PostbackEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        id = None
        if event.source.type == "group":
            id = event.source.group_id
        elif event.source.type == "user":
            id = event.source.user_id

        db = DB()
        clan_id = db.get_clan_by_group_id(id)
        db.close()
        res = event.postback.data
        user = line_bot_api.get_profile(event.source.user_id)
        reply_text = f"{user.display_name} 查詢\n\n"
        if res == "action=Setting":
            text = setting.content
            
            if clan_id == None:
                text += "\n尚未設定部落\n"
            else:
                clan = Clan(clan_id)
                text += f"\n已設定部落：{clan.clan_info()['name']}\n"
                
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=text)]
            ))
            return "OK"
        
        elif res == "action=Introduce":
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=setting.introduce)]
            ))
            return "OK"
        
        if clan_id == None:
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text="尚未設定部落")]
            ))
            return
        clan = Clan(clan_id)
        if res == "action=Capital_Info":
            data = clan.clan_capital_info()
            if data["state"] == "ongoing":
                reply_text += f"突襲 {data['attack_member_nums']}/50，尚有 {50 - data['attack_member_nums']} 個名額\n\n"
                reply_text += f"總首都幣：{data['capitalTotalLoot']}\n"
                reply_text += f"總攻擊數：{data['totalAttacks']}\n\n"
                reply_text += "尚未完成名單：\n"
                
                count = 1
                for i in data["member_list"]:
                    if i["attack_times"] < i["total_attack_nums"]:
                        reply_text += f"{count}. {i['name']} {i['attack_times']}/{ i['total_attack_nums']}\n"
                        count += 1
            elif data["state"] == "ended":
                reply_text += "突襲已結束\n"
             
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))
            
        elif res == "action=Capital_not_start":
            print("Capital_not_start")
            data = clan.clan_capital_not_start()
            
            if data["state"] == "ongoing":
                reply_text += f"突襲 {data['attack_member_nums']}/50，尚有 {50 - data['attack_member_nums']} 個名額\n"
                reply_text += "尚未進攻的成員：\n"
                count = 1           
                for i in data["member_list"]:
                    reply_text += f"{count}. {i['name']}\n"
                    count += 1
                    
            elif data["state"] == "ended":
                reply_text += "突襲已結束\n"
                
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))
            
        elif res == "action=War":
            data = clan.clan_war_not_end()
            if data["state"] == "warEnded":
                reply_text += f"部落戰已於台北時間 {data['end_time']['hours_taipei']}:{data['end_time']['minutes_taipei']} 結束\n\n"
                if data["final"] == 1:
                    reply_text += "勝利\n"
                elif data["final"] == -1:
                    reply_text += "失敗\n"
                elif data["final"] == 0:
                    reply_text += "平手\n"
                reply_text += f"{data['ours']['stars']}-{data['theirs']['stars']}\n\n"
                reply_text += "未進攻的成員：\n"
            elif data["state"] == "inWar":
                reply_text += f"部落戰將於台北時間 {data['end_time']['hours_taipei']}:{data['end_time']['minutes_taipei']} 結束\n"
                reply_text += f"剩餘 {data['end_time']['hours_remaining']} 小時 {data['end_time']['minutes_remaining']} 分 \n\n"
                reply_text += f"目前星數：{data['ours']['stars']} - {data['theirs']['stars']}（總星數：{data['max_stars']}）\n\n"
                reply_text += f"對手尚未三星成員：{data['not_three_starred_opponent_members']} 位\n\n"
                reply_text += "尚未進攻的成員：\n"
            
            elif data["state"] == "preparation":
                reply_text += f"部落戰將於台北時間 {data['end_time']['hours_taipei']}:{data['end_time']['minutes_taipei']} 開始\n"
                reply_text += f"剩餘 {data['end_time']['hours_remaining']} 小時 {data['end_time']['minutes_remaining']} 分 \n\n"
            
            elif data["state"] == "notInWar":
                reply_text += "尚未參與部落戰\n"
            
            # only in war or war ended to display member list
            if data["state"] == "warEnded" or data["state"] == "inWar":
                count = 1
                for i in data["member_list"]:
                    reply_text += f"{count}. {i['name']} {i['attack_times']}/2\n"
                    count += 1
                
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))
        
        elif res == "action=Cwl":
            reply_text += ""
            data = clan.clan_cwl()
            print(data)
            if data == None or data["state"] == "preparation":
                reply_text += "尚未進行聯賽\n"
            elif data["state"] == "inWar":
                reply_text += f"聯賽進行中\n"
                reply_text += f"剩餘 {data['end_time']['hours_remaining']} 小時 {data['end_time']['minutes_remaining']} 分\n\n"
                reply_text += f"目前星數：{data['ours']['stars']} - {data['theirs']['stars']}\n\n"
                if len(data["member_list"]) == 0:
                    reply_text += "全員皆完成部落聯賽\n"
                else:
                    reply_text += "尚未進攻的成員：\n"
                    count = 1
                    for i in data["member_list"]:
                        reply_text += f"{count}. {i['name']}\n"
                        count += 1
                
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))
    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(ReplyMessageRequest(
            reply_token = event.reply_token, 
            messages=[TextMessage(text=setting.introduce)]
        ))
    return 'OK'

scheduler = BackgroundScheduler()
# 10 minutes
db = DB()
scheduler.add_job(func= db.pulse, trigger="interval", minutes=1)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
