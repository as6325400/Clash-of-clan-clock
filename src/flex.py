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
                        "label": "Capital Not yet ended",
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
                        "type": "postback",
                        "label": "Setting",
                        "data": "action=Setting"
                    },
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "Introduce",
                        "data": "action=Introduce"
                    },
                    "height": "sm"
                }
            ],
            "flex": 0
        }
    }
}
