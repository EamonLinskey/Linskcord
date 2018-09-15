import os
import requests
import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

#Preset Messages  and channels to default appear on first load
channels = {"LinscordAbout":[["Hey Welcome to Linscord", "Linscord", '9-11-2018 18:33', '1'], ["This is how messages work", "Linscord", '9-11-2018 18:34', '2']], "The Big Bad Wolf":[]}
users = []

#socket functions can apparently access global arrays nut not gloabl ints so count is sotred as a array
id_count = [2]

@app.route("/")
def index():
    return render_template("index.html", channels=json.dumps(channels))

#Makes a new channel
@socketio.on("submit channel")
def submitChannel(channel):
	if channel not in channels:
		channels[str(channel)] = []
	emit("channel list", channels, broadcast=True)
	
#Submits new messages
@socketio.on("submit message")
def submitMessage(arr):
	# gives each message a unique id
	id_count[0] += 1;
	arr.extend(id_count)
	channels[arr[0]].append(arr[1:])

	#Deletes oldest message if more than 200 in channal
	if len(channels[arr[0]]) > 100:
		channels[arr[0]].pop(0)
	emit("message update", channels, broadcast=True)	

#deletes specifi message by id
@socketio.on("delete message")
def deleteMessage(messId, channel):
	for message in channels[str(channel)]:
		print(message[3])
		if str(message[3])a == str(messId):
			print(message)
			channels[str(channel)].remove(message)
	emit("message update", channels, broadcast=False)

#returns most recent channels to one user
@socketio.on("update messages")
def updateMessages():
	emit("message update", channels, broadcast=False)

#Checks if user in database
@socketio.on("submit user")
def submitUser(user):
	if user in users:
		emit("new user", False, broadcast=False)
	else:
		users.append(user)
		emit("new user", True, broadcast=False)
	
	
