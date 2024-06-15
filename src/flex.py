flex_message = {
    "type": "flex",
    "altText": "coc clock",  # alt_text
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
                        "label": "War",
                        "data": "action=War"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "Not yet ended",
                        "data": "action=Capital_not_end"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "Capital Not Start",
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
                        "type": "uri",
                        "label": "Setting",
                        "uri": "http://linecorp.com/"
                    },
                    "height": "sm"
                }
            ],
            "flex": 0
        }
    }
}
