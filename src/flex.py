flex_message = {
    "type": "flex",
    "altText": "clock",
    "contents": {
        "type": "bubble",
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "0px",
            "spacing": "none",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "none",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://raw.githubusercontent.com/as6325400/Clash-of-clan-clock/refs/heads/main/src/img/image_part_001.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "flex": 1,
                            "action": {"type": "postback", "data": "action=Cwl"},
                        },
                        {
                            "type": "image",
                            "url": "https://raw.githubusercontent.com/as6325400/Clash-of-clan-clock/refs/heads/main/src/img/image_part_002.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "flex": 1,
                            "action": {
                                "type": "postback",
                                "data": "action=Capital_Info",
                            },
                        },
                        {
                            "type": "image",
                            "url": "https://raw.githubusercontent.com/as6325400/Clash-of-clan-clock/refs/heads/main/src/img/image_part_003.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "flex": 1,
                            "action": {"type": "postback", "data": "action=Setting"},
                        },
                    ],
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "none",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://raw.githubusercontent.com/as6325400/Clash-of-clan-clock/refs/heads/main/src/img/image_part_004.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "flex": 1,
                            "action": {"type": "postback", "data": "action=War"},
                        },
                        {
                            "type": "image",
                            "url": "https://raw.githubusercontent.com/as6325400/Clash-of-clan-clock/refs/heads/main/src/img/image_part_005.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "flex": 1,
                            "action": {
                                "type": "postback",
                                "data": "action=Capital_not_start",
                            },
                        },
                        {
                            "type": "image",
                            "url": "https://raw.githubusercontent.com/as6325400/Clash-of-clan-clock/refs/heads/main/src/img/image_part_006.jpg",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "flex": 1,
                            "action": {"type": "postback", "data": "action=Introduce"},
                        },
                    ],
                },
            ],
        },
    },
}
