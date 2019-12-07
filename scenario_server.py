"""
ボタンが押されるたびにシナリオを進めていく
無限ループ
https://docs.google.com/document/d/1JIYEfG2ZTI6NfGATaiU8_lb_NEhzdRq4IDlNlbcsc2I/edit
"""
import os
import json
import subprocess
from time import sleep

import paho.mqtt.client as mqtt

from gen_scenario import scenario
# from gen_scenario import scenario_demo as scenario
from cam_capture import capture
from push_line import push_text_and_image
from tweet import tweet_text_and_image, gen_random_message

#     scenario = json.load(f)

# シナリオのステート
scenario_p = 0

line_firends = [
    "Uac9f94f806d1a634014857766178d4d5", #ogawa
    # "Uca32e9f568b4f13246c6ba1e13bdf000", #sayu
    # "U4c8302e5ec187299150434212954e1ba", #shuto
]

# 音声の再生
def aplay(client, fpath):
    # M5stackにpublishする
    print(fpath)
    client_pub.publish("/sub/M5Stack", "/assets/" + fpath)

    # pcから再生
    print(f"play: {fpath}")
    # cmd = f"aplay assets/mp3/{fpath} -r 1.5"
    cmd = f"mpg123 assets/mp3/{fpath} -q"
    subprocess.call(cmd.split(" "))

def on_connect_pub(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

def on_connect_sub(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("key")
    client.subscribe("/pub/M5Stack")

def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload.decode()) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    global scenario_p
    scenario_p = scenario_p % len(scenario)

    ch = msg.payload.decode()
    if ch == 'A':
        ch = "y"
    elif ch == 'C':
        ch = "n"

    if ch not in ['y', 'n']:
        return

    while True:
        cmd = scenario[scenario_p]["cmd"]
        # 使うデータ
        data = scenario[scenario_p]["data"]
        # 次に行くステート
        jump = scenario[scenario_p].get("next", 1)
        # テキストならプリント
        if cmd == "texts":
            for t in data:
                print(t)
                # client.publish("text", t)
        # つぎに進むシナリオへじゃんぷする
        elif cmd == "pause":
            print("pause")
            scenario_p += jump
            break
        # 分岐をここでチェックしている
        elif cmd == "yes-no":
            if ch == "y":
                scenario_p += data[0]
            else:
                scenario_p += data[1]
            continue
        # 少しとまる
        elif cmd == "sleep":
            for i in range(data, 0, -1):
                print(f"sleep: {i} [sec]")
                sleep(1)
        # 音声再生
        elif cmd == "audio":
            # for t in data:
            # print(t)
            aplay(client, data)
        # 写真撮影
        elif cmd == "photo":
            print("start")
            global fpath
            fpath, fthumb = capture()
            # print("middle")
            endpoint = os.getenv("NGROK_ENDPOINT")
            url = endpoint + fpath
            url_thumb = endpoint + fthumb
            # # print(url, url_thumb)
            # print("end")
            # push_text_and_image(line_firends, "写真撮れたよ〜", url, url_thumb)
            print("LINE:")
            print(line_firends)
            print("写真撮れたよ〜", url, url_thumb)
            pass
        # tweetする
        elif cmd == "tweet":
            print("TWEET:")
            print(gen_random_message())
            print("static/" + fpath)
            # tweet_text_and_image(gen_random_message(), "static/" + fpath)
        else:
            print(f"unknown command: {cmd}")
        scenario_p += jump
        scenario_p = scenario_p % len(scenario)

if __name__ == '__main__':
    # print(json.dumps(scenario, indent=2, ensure_ascii=False))

    client_pub = mqtt.Client()
    client_pub.on_connect = on_connect_pub
    client_pub.on_disconnect = on_disconnect
    client_pub.on_publish = on_publish

    client_pub.connect("localhost", 1883, 60)
    client_pub.loop_start()

    client_sub = mqtt.Client()
    client_sub.on_connect = on_connect_sub
    client_sub.on_disconnect = on_disconnect
    client_sub.on_message = on_message

    client_sub.connect("localhost", 1883, 60)
    client_sub.loop_start()

    while True:
        sleep(1)
