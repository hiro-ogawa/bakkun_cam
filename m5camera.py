from time import sleep
import requests


class M5Camera(object):
    def __init__(self, host):
        self.host = host

    def get_control(self, var, val):
        res = requests.get(f"http://{self.host}/control?var={var}&val={val}")
        return res

    def capture(self):
        res = requests.get(f"http://{self.host}/capture")
        return res

    def set_ae_level(self, ae_level):
        self.get_control("ae_level", ae_level)

    def set_framesize(self, framesize):
        self.get_control("framesize", framesize)

    def set_vflip(self, vflip):
        self.get_control("vflip", vflip)


if __name__ == "__main__":
    cam = M5Camera("192.168.179.3")

    cam.set_ae_level(2)
    cam.set_vflip(1)
    cam.set_framesize(10)
    sleep(0.5)

    res = cam.capture()
    print(res.status_code)

    if res.status_code == 200:
        with open("raw.jpg", "wb") as f:
            f.write(res.content)
