import os
import random
import urllib.parse

import tweepy

access_token = os.getenv("TWITTER_AT")
access_token_secret = os.getenv("TWITTER_ATS")
api_key = os.getenv("TWITTER_CK")
api_secret = os.getenv("TWITTER_CSK")

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

hashtags = ["養老乃瀧池袋南口店", "バックンカメラ", "EpsonPrint", "no1"]
hashtags = [f" #{tag}" for tag in hashtags]
hashtag_text = "".join(hashtags)

random_messages = [
    f"養老乃瀧なう。バックンカメラで写真を撮ったよ！{hashtag_text}\nバックン「こんにちは！バクハイオリジナルキャラクターのバックンだよ。養老乃瀧に遊びに来てね」",
    f"養老乃瀧で、乾杯したよ！{hashtag_text}\nバックン「一軒目酒場も養老乃瀧系列なんだよ！知ってた？？」",
    f"ただいま養老乃瀧で盛り上がってます！{hashtag_text}\nバックン「池袋南口店には、ロボットアニメがいつでも流れているロボ酒場もあるんだよ！」",
    f"養老乃瀧でおいしいご飯を食べているよ！{hashtag_text}\nバックン「僕のオススメは鶏ももジャンボ唐揚だよ！」",
    f"養老乃瀧で、楽しく宴会中！{hashtag_text}\nバックン「養老乃瀧オリジナルカクテルハイボール「バクハイ」の中身は、生ビール&ウイスキー。いい感じに酔えそうだよね」",
    f"養老乃瀧で素敵な笑顔の写真が撮れたよ！{hashtag_text}\nバックン「急に笑顔でカメラを見てねって言われても自然な笑顔になれないみなさんです。ご査収ください。」",
    f"養老乃瀧で仲間と写真を撮ったよ！{hashtag_text}\nバックン「養老乃瀧の由来は、創業者が、その名前の地名に伝わる親孝行伝説からとったんだよ。これ豆だけど、誰も覚えて帰ってくれないだろうな。」",
]


def gen_random_message() -> str:
    return random.choice(random_messages)


def tweet_text_and_image(text, fpath):
    api.update_with_media(filename=fpath, status=text)


def gen_tweet_url(hashtags=[]):
    tags = ",".join([urllib.parse.quote(tag) for tag in hashtags])
    url = f"https://twitter.com/intent/tweet?hashtags={tags}"
    return url


if __name__ == "__main__":
    # tweet_text_and_image("testing", "static/test.jpg")

    # text = 'バックンだよ'
    # statusUpdate = t.statuses.update(status=text)

    # # 生の投稿データの出力
    # print(statusUpdate)

    # # 要素を絞った投稿データの出力
    # print(statusUpdate['user']['screen_name'])
    # print(statusUpdate['user']['name'])
    # print(statusUpdate['text'])

    # print(hashtag_text)
    # for msg in random_messages:
    #     print(msg)
    #     print("")

    tags = [
        "養老乃瀧池袋南口店",
        "バックンカメラ",
        "EpsonPrint",
        "no1",
    ]
    url = gen_tweet_url(tags)
    print(url)
