flex_message = {
    "type": "flex",
    "altText": "test",  # alt_text
    "contents": {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://line.me/"
            }
        },
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
                        "label": "Capital",
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
