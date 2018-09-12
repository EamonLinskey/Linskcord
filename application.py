import os
import requests
import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {"LinscordAbout":[["Hey Welcome to Linscord", "Linscord", '9-11-2018 18:33:4'], ["This is how messages work", "Linscord", '9-11-2018 18:34:2']], "The Big Bad Wolf":[]}

@app.route("/")
def index():
    return render_template("index.html", channels=json.dumps(channels))


@socketio.on("submit channel")
def submitChannel(channel):
	print(channel)
	if channel not in channels:
		channels[str(channel)] = []
	print(channels)
	emit("channel list", channels, broadcast=True)
	

@socketio.on("submit message")
def submitMessage(arr):
	if len(arr) == 4:
		print(channels)
		print(arr)
		channels[arr[0]].append(arr[1:])
		print(channels)
	emit("message update", channels, broadcast=True)


@socketio.on("update messages")
def updateMessages():
	emit("message update", channels, broadcast=False)
	
	
