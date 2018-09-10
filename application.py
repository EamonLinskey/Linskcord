import os
import requests
import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {"LinskcordAbout":[], "The Big Bad Wolf":[]}

@app.route("/")
def index():
    return render_template("index.html", channels=json.dumps(channels))


@socketio.on("submit channel")
def channel(channel):
	print(channel)
	if channel not in channels:
		channels[channel] = []
	print(channels)
	emit("channel list", channels, broadcast=True)
	
