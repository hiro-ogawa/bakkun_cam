import os
from time import sleep
from datetime import datetime
import random

import cv2

from m5camera import M5Camera
from image_handling import add_frame, gen_thumbnail
from push_line import push_text_and_image
from tweet import tweet_text_and_image, gen_random_message

from scenario_server import load_users


def cap(fname="raw.jpg"):
    cam = M5Camera("10.46.31.61")

    cam.set_ae_level(2)
    cam.set_vflip(1)
    cam.set_framesize(10)
    sleep(0.5)

    res = cam.capture()
    print(res.status_code)

    if res.status_code == 200:
        with open(fname, "wb") as f:
            f.write(res.content)


def webcam_cap(fname="raw.jpg"):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    _, dst = cap.read()
    cv2.imwrite(fname, dst)


if __name__ == "__main__":
    cap()
    # webcam_cap()

    frames = [
        "assets/frame2.png",
        "assets/frame_bakuhai.png",
    ]

    # input_fname = "raw_test_image.jpg"
    input_fname = "raw.jpg"

    # frame_fname = "assets/frame2.png"
    # frame_fname = "assets/frame_bakuhai.png"
    frame_fname = random.choice(frames)

    date_str = datetime.now().strftime('%y%m%d_%H%M%S')
    fpath = f"static/{date_str}.jpg"
    ftpath = f"static/{date_str}_thumb.jpg"

    image = add_frame(input_fname, frame_fname)
    print(image.size)
    image.save(fpath)
    thumb = gen_thumbnail(image, (240, 240))
    thumb.save(ftpath)

    uids = load_users()
    # uids = db.get_users("test_group")
    if len(uids):
        furl = os.getenv("NGROK_ENDPOINT") + "/" + fpath
        fturl = os.getenv("NGROK_ENDPOINT") + "/" + ftpath
        push_text_and_image(uids, "testing", furl, fturl)
        print(furl)
        print(fturl)

    msg = gen_random_message()
    tweet_text_and_image(msg, fpath)
