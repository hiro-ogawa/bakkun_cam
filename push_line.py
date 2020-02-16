import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    URIAction,
)

from tweet import gen_tweet_url
# from db_tiny import BakkunDB
# db = BakkunDB()

owners = [
    # "Uca32e9f568b4f13246c6ba1e13bdf000",  # sayu
    # "Uda900fc1da8c3da351d9b9c884aa52e5",  # kyan
    # "U4c8302e5ec187299150434212954e1ba",  # shuto
    "Uac9f94f806d1a634014857766178d4d5",  # ogawa
]
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def push_text_and_image(to, text: str, url: str, thumb_url=None):
    if thumb_url is None:
        thumb_url = url

    tags = [
        "養老乃瀧池袋南口店",
        "バックンカメラ",
        "EpsonPrint",
    ]

    table_no = os.getenv('TABLE_NO', 0)
    tags.append(f"no{table_no}")

    tweet_url = gen_tweet_url(tags)

    msgs = []
    msgs.append(TemplateSendMessage(
        alt_text='撮影完了',
        template=ButtonsTemplate(
            title='撮影完了',
            text=text,
            actions=[
                URIAction(
                    label='Tweetする',
                    uri=tweet_url
                )
            ]
        )
    ))
    # msgs.append(TextSendMessage(text))
    msgs.append(ImageSendMessage(url, thumb_url))
    line_bot_api.multicast(to, msgs)


if __name__ == "__main__":
    # push_text_and_image(owners, "testing", os.getenv(
    #     "NGROK_ENDPOINT") + "test.jpg")

    # uids = db.get_group_members("test_group")
    # if len(uids):
    #     push_text_and_image(uids, "testing", os.getenv(
    #         "NGROK_ENDPOINT") + "/static/test.jpg")

    pass
