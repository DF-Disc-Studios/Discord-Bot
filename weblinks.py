from flask import Flask, request
from threading import Thread
import re
import json
import pymongo
import os

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
database = f"mongodb+srv://{username}:{password}@cluster0.buvu1.mongodb.net/database?retryWrites=true&w=majority"
database = pymongo.MongoClient(database)

app = Flask(__name__)

@app.route("/ping")
def ping_weblink():
  return "Pong"

@app.route("/update/plot", methods=["POST"])
def update_plot_weblink():
  text = re.sub("\u00A7.","",str(request.data, "utf-8"))
  text = text.split("✦")

  if text[12] != os.environ["SPECIAL_KEY"]:
    return "Invalid key"

  json = {
    "_id" : text[0],
    "name" : text[1],
    "owner" : text[2],
    "node" : text[3],
    "tags" : text[4],
    "autoClear" : text[5],
    "lastActive" : text[6],
    "whitelisted" : text[7],
    "playerCount" : text[8],
    "currentVotes" : text[9],
    "barrelLoc" : text[10],
    "icon" : text[11]
  }
  data = database.discStudiosBot.plotData.find_one({"_id":text[0]})
  if data != None:
    database.discStudiosBot.plotData.delete_one({"_id":text[0]})
  
  database.discStudiosBot.plotData.insert_one(json)
  return json

def run():
  app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()