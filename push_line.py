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

owners = [
    "Uac9f94f806d1a634014857766178d4d5",
]
line_bot_api = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))

def push_text_and_image(to, text, url, thumb=None):
    if thumb is None:
        thumb = url

    msgs = []
    msgs.append(TextSendMessage(text))
    msgs.append(ImageSendMessage(url, thumb))
    line_bot_api.multicast(to, msgs)

if __name__ == "__main__":
    push_text_and_image(owners, "testing", os.getenv("NGROK_ENDPOINT") + "test.jpg")
