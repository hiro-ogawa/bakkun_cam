import os
import random

import tweepy

access_token = os.getenv("TWITTER_AT")
access_token_secret = os.getenv("TWITTER_ATS")
api_key = os.getenv("TWITTER_CK")
api_secret = os.getenv("TWITTER_CSK")

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

random_messages = [
    "養老乃瀧で乾杯したよ！ #養老乃瀧 #yorohack\nバックン「乾杯するより一刻も早く飲みたいって人が２人くらいはいそうだね。」",
    "養老乃瀧でおいしい唐揚げを食べているよ！ #養老乃瀧 #yorohack\nバックン「たぶん、ここに写っている大多数はレモンの汁を絞らない派だね。レモンの皮を下にして絞るといいって聞いたけど、そんなに違い感じるかな？」",
    "養老乃瀧で飲み始めて、２時間が経過したよ！ #養老乃瀧 #yorohack\nバックン「養老乃瀧は63年も続く老舗なのに、この中の誰もそれを知らないんじゃないの？」",
    "養老乃瀧で素敵な笑顔の写真が撮れたよ！ #養老乃瀧 #yorohack\nバックン「急に笑顔でカメラを見てねって言われても自然な笑顔になれないみなさんです。ご査収ください。」",
    "養老乃瀧で素敵な仲間と写真が撮れたよ！＃養老乃滝 #yorohack\nバックン「養老乃瀧って、別に養ってもらっても、老人でもないんだよ。創業者が、その名前の地名に伝わる親孝行伝説からとったんだよ。これ豆だけど、誰も覚えて帰ってくれないだろうな。」",
]


def gen_random_message() -> str:
    return random.choice(random_messages)


def tweet_text_and_image(text, fpath):
    api.update_with_media(filename=fpath, status=text)


if __name__ == "__main__":
    tweet_text_and_image("testing", "static/test.jpg")

    # text = 'バックンだよ'
    # statusUpdate = t.statuses.update(status=text)

    # # 生の投稿データの出力
    # print(statusUpdate)

    # # 要素を絞った投稿データの出力
    # print(statusUpdate['user']['screen_name'])
    # print(statusUpdate['user']['name'])
    # print(statusUpdate['text'])
