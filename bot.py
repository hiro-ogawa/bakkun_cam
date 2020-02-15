import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError,
)
from linebot.models import *

from db_tiny import BakkunDB

app = Flask(__name__)

# 環境変数読み込み
line_channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_channel_secret = os.environ['LINE_CHANNEL_SECRET']
debug = os.environ.get('DEBUG', 'False') == 'True'

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

db = BakkunDB()


@app.route("/callback", methods=['POST'])
def callback():
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


def is_connection_check(event):
    check_uid = 'Udeadbeefdeadbeefdeadbeefdeadbeef'
    check_tokens = [
        '00000000000000000000000000000000',
        'ffffffffffffffffffffffffffffffff',
    ]
    if event.source.type == 'user':
        if event.source.user_id == check_uid:
            return True
    if event.reply_token in check_tokens:
        return True
    return False


@handler.default()
def default(event):
    print("default method")

    print(event)
    if is_connection_check(event):
        return


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if is_connection_check(event):
        return
    print(event)

    text = event.message.text

    reply_msgs = []

    uid = event.source.user_id
    # キーワードチェック
    if text == "JOIN:GROUP1":
        db.add_user_to_group(uid, "group1")
    elif text == "JOIN-GROUP2":
        db.add_user_to_group(uid, "group2")
    elif text == "バイバイ GROUP1":
        db.delete_group("group1")
    elif text == "バイバイ GROUP2":
        db.delete_group("group2")

    elif text == "ばいばい":
        db.delete_group("test_group")
        reply_msgs.append(TextSendMessage(
            text="実証実験に協力してくれてありがとう。\nグループを削除したよ。"))
    else:
        # グループDB更新
        db.add_user_to_group(uid, "test_group")

        reply_msgs.append(TextSendMessage(text="バックンカメラの実証実験へようこそ。グループの全員がお友達になったら開始ボタンを押してね", quick_reply=QuickReply(items=[
            QuickReplyButton(action=PostbackAction(label="開始", data="start"))
        ])))

        # mqttで開始コマンド送信

    line_bot_api.reply_message(event.reply_token, reply_msgs)


@handler.add(FollowEvent)
def handle_follow_event(event):
    print(event)

    # ユーザDB更新
    uid = event.source.user_id
    profile = line_bot_api.get_profile(uid)
    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
    user = {
        "name": profile.display_name,
        "uid": profile.user_id,
        "picture_url": profile.picture_url,
        "status_message": profile.status_message,
        "follow": True,
    }
    db.update_user(user)

    # 返信
    reply_msgs = []
    reply_msgs.append(TextSendMessage(
        text="友達になってくれてありがとう\nバックンカメラを開始するにはQRコードで合言葉を入れてね"))
    line_bot_api.reply_message(event.reply_token, reply_msgs)


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    print(event)

    # ユーザDB更新
    uid = event.source.user_id
    db.unfollow_user(uid)


@handler.add(PostbackEvent)
def handle_postback_event(event):
    print(event)

    reply_msgs = []
    if event.postback.data == "start":
        reply_msgs.append(TextSendMessage(text="バックンカメラの実証実験を開始します\n楽しんでいってね"))

    if len(reply_msgs):
        line_bot_api.reply_message(event.reply_token, reply_msgs)


if __name__ == "__main__":
    app.run(debug=debug)
