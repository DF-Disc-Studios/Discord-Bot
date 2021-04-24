from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/ping")
def ping_weblink():
  return "Pong"

def run():
  app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()