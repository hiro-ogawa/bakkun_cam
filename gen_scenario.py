"""
https://docs.google.com/document/d/1JIYEfG2ZTI6NfGATaiU8_lb_NEhzdRq4IDlNlbcsc2I/edit
"""
import json

"""
b1_いらっしゃいませ、ようこそ養老乃瀧へ.wav
b2_僕の名前はバックン、よろしくね.wav
b3_飲み物はそろったかな.wav
b4_ねえねえ、記念写真を撮らない？.wav
b5_おっけー！じゃあ上のカメラを見てね。3.2.1.はい、撮れたよー.wav
b6_撮るならイエスボタン、撮らないならノーボタンを押してね.wav
b7_シェアする？するならイエスボタン、しないならノーボタンを押してね.wav
b8_シェアしたよ、僕の一言コメントもチェックしてね.wav
b9_シェアはしないんだね、わかったよ.wav
b10_えー？じゃあ、後で撮ろうね.wav
b11_そろそろ美味しいご飯と一緒に写真を撮ろうよ.wav
b12_いいね、じゃあ上のカメラを見ておいしそうな顔をして！3.2.1.はい、撮れたよ〜.wav
b13_まあ、最後に記念撮影っていうのもアリかもね〜.wav
b14_さあ、みんなで最後に写真を撮ろうよ.wav
b15_チッ(最後に写真を撮らなかった).wav
b16_今日は来てくれてありがとう！また遊ぼうね.wav
b17_それじゃあ、またねー.wav
b18_ゆっくり楽しんでいってね.wav
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
        "data": "assets/wav/b1.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b2.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b3.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b4.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b6.wav",
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
        "data": "assets/wav/b22.wav",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b21.wav",
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
        "data": "assets/wav/b7.wav",
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
        "data": "assets/wav/b8.wav",
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
        "data": "assets/wav/b9.wav",
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
        "data": "assets/wav/b10.wav",
    },

    {
        "cmd": "texts",
        "data": [
            "ゆっくり楽しんでいってね",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b18.wav",
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
        "data": "assets/wav/b11.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b6.wav",
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
        "data": "assets/wav/b19.wav",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b21.wav",
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
        "data": "assets/wav/b7.wav",
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
        "data": "assets/wav/b8.wav",
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
        "data": "assets/wav/b9.wav",
    },
    {
        "cmd": "texts",
        "data": [
            "それじゃあ、またねー",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b17.wav",
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
        "data": "assets/wav/b13.wav",
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
        "data": "assets/wav/b14.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b6.wav",
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
        "data": "assets/wav/b20.wav",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b21.wav",
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
        "data": "assets/wav/b7.wav",
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
        "data": "assets/wav/b8.wav",
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
        "data": "assets/wav/b9.wav",
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
        "data": "assets/wav/b15.wav",
    },
    {
        "cmd": "texts",
        "data": [
            "今日は来てくれてありがとう！また遊ぼうね！！",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b16.wav",
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
        "data": "assets/wav/b11.wav",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b6.wav",
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
        "data": "assets/wav/b19.wav",
    },
    {
        "cmd": "photo",
        "data": "",
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b21.wav",
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
        "data": "assets/wav/b7.wav",
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
        "data": "assets/wav/b8.wav",
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
        "data": "assets/wav/b9.wav",
    },
    {
        "cmd": "texts",
        "data": [
            "それじゃあ、またねー",
        ],
    },
    {
        "cmd": "audio",
        "data": "assets/wav/b17.wav",
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
        "data": "assets/wav/b13.wav",
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

with open("assets/wav/scenario.json", "wt") as f:
    json.dump(scenario, f, indent=2, ensure_ascii=False)
