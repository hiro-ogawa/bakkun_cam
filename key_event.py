"""
キーイベントを送信するだけ
"""

import sys
import termios
import paho.mqtt.client as mqtt
from time import sleep

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print(f"publish #{mid}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.connect("localhost", 1883, 60)

    client.loop_start()

    #標準入力のファイルディスクリプタを取得
    fd = sys.stdin.fileno()

    #fdの端末属性をゲットする
    #oldとnewには同じものが入る。
    #newに変更を加えて、適応する
    #oldは、後で元に戻すため
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)

    #new[3]はlflags
    #ICANON(カノニカルモードのフラグ)を外す
    new[3] &= ~termios.ICANON
    #ECHO(入力された文字を表示するか否かのフラグ)を外す
    new[3] &= ~termios.ECHO


    try:
        # 書き換えたnewをfdに適応する
        termios.tcsetattr(fd, termios.TCSANOW, new)

        while True:
            # キーボードから入力を受ける。
            # lfalgsが書き換えられているので、エンターを押さなくても次に進む。echoもしない
            ch = sys.stdin.read(1)
            print(f"publish: {ch}")
            client.publish("key", ch)
            if ch == "q":
                break

    finally:
        # fdの属性を元に戻す
        # 具体的にはICANONとECHOが元に戻る
        termios.tcsetattr(fd, termios.TCSANOW, old)

if __name__ == '__main__':
    main()
