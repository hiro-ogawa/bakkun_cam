from datetime import datetime
import random
import cv2
import numpy as np

frames = [
    # "assets/frame2.png",
    # "assets/frame_bakuhai.png",
    "assets/frame_festa.png",
]

img_w = 1280
img_h = 720

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 30)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_w)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_h)

def capture():
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_h)

    ret, dst = cap.read()

    cap.release

    dst = cv2.resize(dst, (img_w, img_h))
    # dst = cv2.rotate(dst, cv2.ROTATE_180)
    cv2.imwrite("cap.jpg", dst)

    # 上下に 420 pix ずつ足す
    white = np.ones((int((img_w - img_h) / 2), img_w, 3), np.uint8)*255
    dst = cv2. vconcat([white, dst, white])

    src = cv2.imread(random.choice(frames), -1)

    mask = src[:,:,3]  # アルファチャンネルだけ抜き出す。
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
    mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。

    src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

    dst = dst * (1 - mask) # 透過率に応じて元の画像を暗くする。
    dst += src * mask  # 貼り付ける方の画像に透過率をかけて加算。

    date_str = datetime.now().strftime('%y%m%d_%H%M%S')
    fname = f"{date_str}.jpg"
    cv2.imwrite("static/" + fname, dst)

    fthumb = f"{date_str}_thumb.jpg"
    cv2.imwrite("static/" + fthumb, cv2.resize(dst, (240, 240)))

    return fname, fthumb

if __name__ == "__main__":
    fpath = capture()
    print(fpath)
