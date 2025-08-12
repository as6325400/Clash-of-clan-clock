flex_message = {
    "type": "flex",
    "altText": "clock",  # alt_text
    "contents": {
        "type": "bubble",
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "部落聯賽",
                        "data": "action=Cwl"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "部落戰",
                        "data": "action=War"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "突襲尚未完成名單",
                        "data": "action=Capital_not_end"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "突襲進攻資訊",
                        "data": "action=Capital_not_start"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "設定教學",
                        "data": "action=Setting"
                    },
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "介紹教學",
                        "data": "action=Introduce"
                    },
                    "height": "sm"
                }
            ],
            "flex": 0
        }
    }
}
