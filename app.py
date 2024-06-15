import os
import sys
from argparse import ArgumentParser

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
from src import flex
from model.clan import Clan

load_dotenv()

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
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        flex_message = flex.flex_message
        if event.message.text.strip() == "clock":
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[FlexMessage.from_dict(flex_message)]
            ))
            
        # else:
        #     user_id = event.source.user_id
        #     profile = line_bot_api.get_profile(user_id)
        #     user_name = profile.display_name
        #     line_bot_api.reply_message_with_http_info(
        #         ReplyMessageRequest(
        #             reply_token=event.reply_token,
        #             messages=[TextMessage(text=f"@{user_name}")]
        #         )
        #     )
        
@handler.add(PostbackEvent)
def handle_message(event: PostbackEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        clan = Clan("#9LY9RLRL")
        res = event.postback.data
        user = line_bot_api.get_profile(event.source.user_id)
        reply_text = f"{user.display_name} 查詢\n\n"
        if res == "action=Capital_not_end":
            print("Capital_not_end")
            data = clan.clan_capital_not_end()
            reply_text += f"突襲{data['attack_member_nums']}/50，尚有 {50 - data['attack_member_nums']}個名額\n"
            count = 1
            for i in data["member_list"]:
                if i["attack_times"] < i["total_attack_nums"]:
                    reply_text += f"{count}. {i['name']} {i["attack_times"]}/{ i["total_attack_nums"]}\n"
                    count += 1
             
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))
        elif res == "action=Capital_not_start":
            data = clan.clan_capital_not_start()
            reply_text += f"突襲{data['attack_member_nums']}/50，尚有 {50 - data['attack_member_nums']}個名額\n"
            reply_text += "尚未打突襲的成員有：\n"
            count = 1
            
            for i in data["member_list"]:
                reply_text += f"{count}. {i['name']}\n"
                count += 1
            
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))
            
        elif res == "action=War":
            data = clan.clan_war_not_end()
            if data["state"] != "inWar":
                reply_text += "目前沒有打戰\n"
            else:
                reply_text += "尚未打戰的成員有：\n"
                count = 1
                for i in data["member_list"]:
                    reply_text += f"{count}. {i['name']} {i['attack_times']}/2\n"
                    count += 1
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token = event.reply_token, 
                messages=[TextMessage(text=reply_text)]
            ))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=port, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, port=options.port)