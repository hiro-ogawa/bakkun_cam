#! /usr/bin/env python3

import io
from time import sleep
from PIL import Image
import requests
from datetime import datetime
import random
import numpy as np
import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

frames = [
    "assets/frame2.png",
    "assets/frame_bakuhai.png",
    # "assets/frame_festa.png",
]

img_w = 1280
img_h = 720


# resolution : 0 QQVGA 〜 10 UXGA 
# flip Boolで縦方向に反転/非反転  
# camera_ip_addr : 192.168.0.xx などカメラのIP addrを指定
def capture_from_m5cam(resolution, flip, camera_ip_addr):
    addr = 'http://' + camera_ip_addr
    ae_control = addr + "/control?var=ae_level&val=2"
    res = requests.get(ae_control)
    if flip is True:
        flip_control = addr + "/control?var=vflip&val=1"
    else:
        flip_control = addr + "/control?var=vflip&val=0"
    res = requests.get(flip_control)
    resolution_control_addr = addr + \
        '/control?var=framesize&val=' + str(resolution)
    res = requests.get(resolution_control_addr)
    sleep(0.7)
    capture_addr = addr + '/capture'
    res = requests.get(capture_addr)
    if res.status_code == 200:
        print("succeeded to get the photo")
    else:
        print("failed to get the photo.")
        return 0, 0
    img = Image.open(io.BytesIO(res.content))
    ocv_img = pil2cv(img)
    dst = scale_to_width(ocv_img, img_w)
    dst = trimming(dst)
    # 上下に 420 pix ずつ足す
    white = np.ones((int((img_w - img_h) / 2), img_w, 3), np.uint8)*255
    dst = cv2. vconcat([white, dst, white])
    src = cv2.imread(random.choice(frames), -1)
    src = scale_to_width(src, img_w)
    mask = src[:, :, 3]  # アルファチャンネルだけ抜き出す。
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
    mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
    src = src[:, :, :3]  # アルファチャンネルは取り出しちゃったのでもういらない。
    dst = dst * (1 - mask)  # 透過率に応じて元の画像を暗くする。
    dst += src * mask  # 貼り付ける方の画像に透過率をかけて加算。
    date_str = datetime.now().strftime('%y%m%d_%H%M%S')
    fname = f"{date_str}.jpg"
    cv2.imwrite("static/" + fname, dst)
    fthumb = f"{date_str}_thumb.jpg"
    cv2.imwrite("static/" + fthumb, cv2.resize(dst, (240, 240)))
    return fname, fthumb


def scale_to_width(img, width):
    scale = width / img.shape[1]
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)


def trimming(img):
    height = img.shape[0]
    return img[int(height / 2 - img_h / 2): int(height / 2 + img_h / 2), :]


def pil2cv(image):
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


if __name__ == "__main__":
    fpath = capture_from_m5cam(
        resolution=10, flip=True, camera_ip_addr="192.168.0.206")
    print(fpath)
