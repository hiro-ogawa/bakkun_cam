from datetime import datetime

import cv2
import numpy as np

def capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    ret, dst = cap.read()
    cv2.imwrite("cap.jpg", dst)


    src = cv2.imread("frame.png", -1)

    mask = src[:,:,3]  # アルファチャンネルだけ抜き出す。
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
    mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。

    src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

    dst = dst * (1 - mask) # 透過率に応じて元の画像を暗くする。
    dst += src * mask  # 貼り付ける方の画像に透過率をかけて加算。

    date_str = datetime.now().strftime('%y%m%d_%H%M%S')
    fname = f"{date_str}.jpg"
    cv2.imwrite("static/" + fname, dst)

    return fname

if __name__ == "__main__":
    fpath = capture()
    print(fpath)
