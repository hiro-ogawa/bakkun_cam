import qrcode
import urllib.parse

line_id = "@652bkyab"
text = "バックンカメラ"
etext = urllib.parse.quote(text)
url = f"line://oaMessage/{line_id}/?{etext}"
print(url)
img = qrcode.make(f"{url}{etext}")

friend_url = f"https://line.me/R/ti/p/{line_id}"

img = qrcode.make(friend_url)
img.save('qr_test.png')
