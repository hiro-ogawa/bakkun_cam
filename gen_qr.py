import qrcode
import urllib.parse

line_id = "@325ccasn"
text = "JOIN:GROUP1"
enc_text = urllib.parse.quote(text)
url = f"line://oaMessage/{line_id}/?{enc_text}"
print(url)
img = qrcode.make(f"{url}")
img.save('line_join_g1.png')

friend_url = f"https://line.me/R/ti/p/{line_id}"

img = qrcode.make(friend_url)
img.save('line_friend.png')
