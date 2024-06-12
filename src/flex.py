flex_message = {
    "type": "flex",
    "altText":"test", #alt_text
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
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "COC Clock",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": []
            }
            ]
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
                "type": "uri",
                "label": "CALL",
                "uri": "https://line.me/"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "uri",
                "label": "WEBSITE",
                "uri": "https://line.me/"
                }
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