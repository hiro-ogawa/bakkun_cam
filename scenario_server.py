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

# with open("assets/scenario.json") as f:
#     scenario = json.load(f)

scenario_p = 0

line_firends = [
    "Uac9f94f806d1a634014857766178d4d5",  # ogawa
    "Uca32e9f568b4f13246c6ba1e13bdf000",  # sayu
    "U4c8302e5ec187299150434212954e1ba",  # shuto
]

usersjson = "users.json"


def aplay(fpath):
    if os.path.exists(fpath):
        print(f"play: {fpath}")
        cmd = f"afplay {fpath} -r 1.5"
        subprocess.call(cmd.split(" "))
        print(f"fin")
    else:
        print(f"file does not exist: {fpath}")


def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("key")
    client.subscribe("user")


def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")


def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload.decode()) +
          "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    if msg.topic == "key":
        handle_scenario(client, msg.payload.decode())
    elif msg.topic == "user":
        handle_user(json.loads(msg.payload.decode()))


def handle_scenario(client, ch):
    global scenario_p
    scenario_p = scenario_p % len(scenario)

    if ch not in ['y', 'n']:
        return

    while True:
        cmd = scenario[scenario_p]["cmd"]
        data = scenario[scenario_p]["data"]
        jump = scenario[scenario_p].get("next", 1)
        if cmd == "texts":
            for t in data:
                print(t)
                client.publish("text", t)
        elif cmd == "pause":
            print("pause")
            scenario_p += jump
            break
        elif cmd == "yes-no":
            if ch == "y":
                scenario_p += data[0]
            else:
                scenario_p += data[1]
            continue
        elif cmd == "sleep":
            for i in range(data, 0, -1):
                print(f"sleep: {i} [sec]")
                sleep(1)
        elif cmd == "audio":
            aplay(data)
        elif cmd == "photo":
            global fpath
            fpath, fthumb = capture()
            endpoint = os.getenv("NGROK_ENDPOINT")
            url = endpoint + fpath
            url_thumb = endpoint + fthumb
            # print(url, url_thumb)
            # push_text_and_image(line_firends, "写真撮れたよ〜", url, url_thumb)
            push_text_and_image(load_users(), "写真撮れたよ〜", url, url_thumb)
        elif cmd == "tweet":
            tweet_text_and_image(gen_random_message(), "static/" + fpath)
        else:
            print(f"unknown command: {cmd}")
        scenario_p += jump
        scenario_p = scenario_p % len(scenario)


def load_users():
    try:
        with open(usersjson) as f:
            return json.load(f)
    except:
        print(f"failed to load {usersjson}")

        return []


def add_user(user):
    users = load_users()
    if user not in users:
        users.append(user)
    with open(usersjson, "w") as f:
        json.dump(users, f)


def handle_user(data):
    cmd = data["cmd"]
    if cmd == "add":
        try:
            uid = data["val"]
        except:
            return

        add_user(uid)
    if cmd == "clear":
        print(f"delete {usersjson}")
        os.remove(usersjson)
    if cmd == "start":
        print("start")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    # print(json.dumps(scenario, indent=2, ensure_ascii=False))
    main()
