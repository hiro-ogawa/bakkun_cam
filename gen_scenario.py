"""
https://docs.google.com/document/d/1JIYEfG2ZTI6NfGATaiU8_lb_NEhzdRq4IDlNlbcsc2I/edit
"""
import json

"""
b1_いらっしゃいませ、ようこそ養老乃瀧へ.mp3
b2_僕の名前はバックン、よろしくね.mp3
b3_飲み物はそろったかな.mp3
b4_ねえねえ、記念写真を撮らない？.mp3
b5_おっけー！じゃあ上のカメラを見てね。3.2.1.はい、撮れたよー.mp3
b6_撮るならイエスボタン、撮らないならノーボタンを押してね.mp3
b7_シェアする？するならイエスボタン、しないならノーボタンを押してね.mp3
b8_シェアしたよ、僕の一言コメントもチェックしてね.mp3
b9_シェアはしないんだね、わかったよ.mp3
b10_えー？じゃあ、後で撮ろうね.mp3
b11_そろそろ美味しいご飯と一緒に写真を撮ろうよ.mp3
b12_いいね、じゃあ上のカメラを見ておいしそうな顔をして！3.2.1.はい、撮れたよ〜.mp3
b13_まあ、最後に記念撮影っていうのもアリかもね〜.mp3
b14_さあ、みんなで最後に写真を撮ろうよ.mp3
b15_チッ(最後に写真を撮らなかった).mp3
b16_今日は来てくれてありがとう！また遊ぼうね.mp3
b17_それじゃあ、またねー.mp3
b18_ゆっくり楽しんでいってね.mp3
"""

scenario_orig = [
    # 来店時
    {
        "cmd": "texts",
        "data": [
            "いらっしゃいませ〜！",
            "ようこそ養老の滝へ！",
            "僕の名前はバックン！よろしくね！",
            "",
            "飲み物は揃ったかな？",
            "ねえねえ、記念写真を撮らない？撮るならイエスボタン、撮らないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b1.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b2.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b3.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b4.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b6.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 14],
    },
    {
        "cmd": "texts",
        "data": [
            "オッケー！じゃあ、上のカメラを見てね。",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b22.mp3",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/b21.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "はい、撮れたよ〜！",
            "シェアする？するならイエスボタン、しないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b7.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 4],
    },
    {
        "cmd": "tweet",
        "data": "",
    },
    {
        "cmd": "texts",
        "data": [
            "シェアしたよ、僕の一言コメントもチェックしてね",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b8.mp3",
        "next": 5,
    },
    {
        "cmd": "texts",
        "data": [
            "シェアはしないんだね、わかったよ",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b9.mp3",
        "next": 3,
    },

    {
        "cmd": "texts",
        "data": [
            "えー！じゃあ、後で撮ろうね！楽しんで〜！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b10.mp3",
    },

    {
        "cmd": "texts",
        "data": [
            "ゆっくり楽しんでいってね",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b18.mp3",
    },

    # {
    #     "cmd": "sleep",
    #     "data": 5,
    # },
    {
        "cmd": "pause",
        "data": "",
    },

    # １時間経過
    {
        "cmd": "texts",
        "data": [
            "そろそろ、美味しいご飯と一緒に写真を撮ろうよ！撮るならイエスボタン、撮らないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b11.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b6.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 16],
    },
    {
        "cmd": "texts",
        "data": [
            "いいね！じゃあ、上のカメラを見て、美味しそうな顔をして！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b19.mp3",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/b21.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "はい、撮れたよ〜！",
            "シェアする？するならイエスボタン、しないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b7.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 4],
    },
    {
        "cmd": "tweet",
        "data": "",
    },
    {
        "cmd": "texts",
        "data": [
            "シェアしたよ、僕の一言コメントもチェックしてね",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b8.mp3",
        "next": 3,
    },
    {
        "cmd": "texts",
        "data": [
            "シェアはしないんだね、わかったよ",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b9.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "それじゃあ、またねー",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b17.mp3",
        "next": 3,
    },

    {
        "cmd": "texts",
        "data": [
            "最後に記念撮影っていうのもアリかもね。",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b13.mp3",
    },

    # {
    #     "cmd": "sleep",
    #     "data": 5,
    # },
    {
        "cmd": "pause",
        "data": "",
    },

    # ２時間半経過
    {
        "cmd": "texts",
        "data": [
            "さあ！みんなで最後に写真を撮ろうよ！撮るならイエスボタン、撮らないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b14.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b6.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 14],
    },
    {
        "cmd": "texts",
        "data": [
            "オッケー！じゃあ、上のカメラを見て、最高の笑顔でね。",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b20.mp3",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/b21.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "はい、撮れたよ〜！",
            "シェアする？するならイエスボタン、しないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b7.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 4],
    },
    {
        "cmd": "tweet",
        "data": "",
    },
    {
        "cmd": "texts",
        "data": [
            "シェアしたよ、僕の一言コメントもチェックしてね",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b8.mp3",
        "next": 5,
    },
    {
        "cmd": "texts",
        "data": [
            "シェアはしないんだね、わかったよ",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b9.mp3",
        "next": 3,
    },

    {
        "cmd": "texts",
        "data": [
            "・・・！！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b15.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "今日は来てくれてありがとう！また遊ぼうね！！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b16.mp3",
    },

    {
        "cmd": "pause",
        "data": "",
    },
    # {
    #     "cmd": "sleep",
    #     "data": 10,
    # },
]

scenario = [
    # １時間経過
    {
        "cmd": "texts",
        "data": [
            "そろそろ、美味しいご飯と一緒に写真を撮ろうよ！撮るならイエスボタン、撮らないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b11.mp3",
    },
    {
        "cmd": "audio",
        "data": "assets/b6.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 16],
    },
    {
        "cmd": "texts",
        "data": [
            "いいね！じゃあ、上のカメラを見て、美味しそうな顔をして！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b19.mp3",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/b21.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "はい、撮れたよ〜！",
            "シェアする？するならイエスボタン、しないならノーボタンを押してね！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b7.mp3",
    },
    {
        "cmd": "pause",
        "data": "",
    },
    {
        "cmd": "yes-no",
        "data": [1, 4],
    },
    {
        "cmd": "tweet",
        "data": "",
    },
    {
        "cmd": "texts",
        "data": [
            "シェアしたよ、僕の一言コメントもチェックしてね",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b8.mp3",
        "next": 3,
    },
    {
        "cmd": "texts",
        "data": [
            "シェアはしないんだね、わかったよ",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b9.mp3",
    },
    {
        "cmd": "texts",
        "data": [
            "それじゃあ、またねー",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b17.mp3",
        "next": 3,
    },

    {
        "cmd": "texts",
        "data": [
            "最後に記念撮影っていうのもアリかもね。",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/b13.mp3",
    },

    # {
    #     "cmd": "sleep",
    #     "data": 5,
    # },
    {
        "cmd": "pause",
        "data": "",
    },
]

with open("assets/scenario.json", "wt") as f:
    json.dump(scenario, f, indent=2, ensure_ascii=False)
