import os
import json

from flask import Flask, request, abort
import paho.mqtt.client as mqtt

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

mqtt_clients = [
    mqtt.Client(),
    mqtt.Client(),
    mqtt.Client(),
]
mqtt_servers = [
    "10.46.31.31",
    "localhost",
    "localhost",
    # "192.168.42.114",
]
groups = [
    "group1",
    "group2",
    "test_group",
]


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
        db.add_user_to_group(uid, groups[0])
        mqtt_clients[0].publish("user", json.dumps({"cmd": "add", "val": uid}))

        reply_msgs.append(TextSendMessage(text="バックンカメラの実証実験へようこそ。グループの全員がお友達になったら開始ボタンを押してね", quick_reply=QuickReply(items=[
            QuickReplyButton(action=PostbackAction(label="開始", data="start"))
        ])))
    elif text == "JOIN-GROUP2":
        db.add_user_to_group(uid, groups[1])
        mqtt_clients[1].publish("user", json.dumps({"cmd": "add", "val": uid}))

        reply_msgs.append(TextSendMessage(text="バックンカメラの実証実験へようこそ。グループの全員がお友達になったら開始ボタンを押してね", quick_reply=QuickReply(items=[
            QuickReplyButton(action=PostbackAction(label="開始", data="start"))
        ])))

    elif text == "バイバイ GROUP1":
        db.delete_group(groups[1])
        mqtt_clients[0].publish("user", json.dumps({"cmd": "clear"}))

        msgs = TextSendMessage(
            text="実証実験に協力してくれてありがとう。\nグループを削除したよ。")
        send_msgs_group(uid, msgs, event.reply_token)
    elif text == "バイバイ GROUP2":
        db.delete_group(groups[1])
        mqtt_clients[1].publish("user", json.dumps({"cmd": "clear"}))

        msgs = TextSendMessage(
            text="実証実験に協力してくれてありがとう。\nグループを削除したよ。")
        send_msgs_group(uid, msgs, event.reply_token)
    elif text == "ばいばい":
        db.delete_group(groups[2])
        mqtt_clients[2].publish("user", json.dumps({"cmd": "clear"}))

        msgs = TextSendMessage(
            text="実証実験に協力してくれてありがとう。\nグループを削除したよ。")
        send_msgs_group(uid, msgs, event.reply_token)

    else:
        # グループDB更新
        db.add_user_to_group(uid, groups[2])
        mqtt_clients[2].publish("user", json.dumps({"cmd": "add", "val": uid}))

        reply_msgs.append(TextSendMessage(text="バックンカメラの実証実験へようこそ。グループの全員がお友達になったら開始ボタンを押してね", quick_reply=QuickReply(items=[
            QuickReplyButton(action=PostbackAction(label="開始", data="start"))
        ])))

    if len(reply_msgs):
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

    uid = event.source.user_id

    if event.postback.data == "start":
        msgs = TextSendMessage(
            text="バックンカメラの実証実験を開始します\n楽しんでいってね")
        send_msgs_group(uid, msgs, event.reply_token)

    # mqtt 開始コマンド送信
    group = db.get_group_from_uid(uid)
    i = groups.index(group)
    mqtt_clients[i].publish("user", json.dumps({"cmd": "start"}))


def send_msgs_group(uid, msgs, reply_token=None):
    group = db.get_group_from_uid(uid)
    if group:
        members = db.get_group_members(group)

        if reply_token:
            members.remove(uid)
            line_bot_api.reply_message(reply_token, msgs)

        if members:
            line_bot_api.multicast(members, msgs)

##############
# MQTT
##############


def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))


def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")


def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


def init_mqtt():
    for i, client in enumerate(mqtt_clients):
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish

        client.connect(mqtt_servers[i], 1883, 60)

        client.loop_start()


if __name__ == "__main__":
    init_mqtt()
    app.run(debug=debug)
