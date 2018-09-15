import os
import requests
import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {"LinscordAbout":[["Hey Welcome to Linscord", "Linscord", '9-11-2018 18:33', '1'], ["This is how messages work", "Linscord", '9-11-2018 18:34', '2']], "The Big Bad Wolf":[]}
users = []
id_count = [2]
print(id_count)

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
	print(channels)
	print(users)
	print(arr)
	print(id_count)
	id_count[0] += 1;
	arr.extend(id_count)
	channels[arr[0]].append(arr[1:])
	
	
	if len(channels[arr[0]]) > 100:
		channels[arr[0]].pop(0)
	print(channels)
	emit("message update", channels, broadcast=True)	

@socketio.on("delete message")
def deleteMessage(messId, channel):
	#print(messId)
	#print(channels[str(channel)])
	print("---------")
	print(messId)
	for message in channels[str(channel)]:
		print(message[3])
		if str(message[3]) == str(messId):
			print(message)
			channels[str(channel)].remove(message)
	emit("message update", channels, broadcast=False)



@socketio.on("update messages")
def updateMessages():
	emit("message update", channels, broadcast=False)

@socketio.on("submit user")
def submitUser(user):
	print(user)
	if user in users:
		emit("new user", False, broadcast=False)
	else:
		users.append(user)
		emit("new user", True, broadcast=False)
	
	
