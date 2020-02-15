import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from db_tiny import BakkunDB
db = BakkunDB()

owners = [
    "Uac9f94f806d1a634014857766178d4d5",
]
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def push_text_and_image(to, text: str, url: str, thumb_url=None):
    if thumb_url is None:
        thumb_url = url

    msgs = []
    msgs.append(TextSendMessage(text))
    msgs.append(ImageSendMessage(url, thumb_url))
    line_bot_api.multicast(to, msgs)


if __name__ == "__main__":
    # push_text_and_image(owners, "testing", os.getenv(
    #     "NGROK_ENDPOINT") + "test.jpg")

    uids = db.get_users("test_group")
    if len(uids):
        push_text_and_image(uids, "testing", os.getenv(
            "NGROK_ENDPOINT") + "/static/test.jpg")
