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
from cam_capture import capture

# with open("assets/scenario.json") as f:
#     scenario = json.load(f)

scenario_p = 0

def aplay(fpath):
    if os.path.exists(fpath):
        print(f"play: {fpath}")
        cmd = f"afplay {fpath} -r 3.0"
        subprocess.call(cmd.split(" "))
        print(f"fin")
    else:
        print(f"file does not exist: {fpath}")

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("key")

def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))

def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    global scenario_p

    ch = msg.payload.decode()
    if ch not in ['y', 'n']:
        return

    while True:
        cmd = scenario[scenario_p]["cmd"]
        data = scenario[scenario_p]["data"]
        jump = scenario[scenario_p].get("next", 1)
        if cmd == "texts":
            for t in data:
                print(t)
        elif cmd == "pause":
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
        # elif cmd == "photo":
        #     fpath = capture()
        #     url = os.getenv("NGROK_ENDPOINT") + fpath
        #     push_line_image(url)
        else:
            print(f"unknown command: {cmd}")
        scenario_p += jump
        scenario_p = scenario_p % len(scenario)

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
