import os
from flask import Flask, request, abort

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=True)
