from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import eventlet

import sqlite3
conn = sqlite3.connect('chatRoom.db')
c = conn.cursor()
c.execute("CREATE TABLE ChatRooms (name TEXT);")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
global id
id=0
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/a/homepage')
def homepage():
	return render_template('homepage.html')

@app.route('/<roomID>/')
def room(roomID):
	return render_template('index.html',room=roomID)

@socketio.on('createRoom')
def create_room():
	while (true):
		#generate chat room name
		roomName = '23q4adsf';
		if (c.execute("SELECT TOP 1 name FROM ChatRooms WHERE name=\""+roomID+"\"" == ""):
		     return "//"+roomID+"//"
	return null
	
@socketio.on('msg')
def handle_msg(msg):
        #Messages are in the form ROOM:::MESSAGE
        print('received ' + msg)
        emit('receive', msg.split(":::")[1], room=msg.split(":::")[0])
        eventlet.sleep(0)

@socketio.on('join')
def on_join(room):
        global id
        id+=1
        join_room(room)
        print(room)
        #emit('confirm', str(id))
        emit('receive', 'User '+str(id)+' has entered the room.', room=room)
        eventlet.sleep(0)        

@socketio.on('disconnect')
def on_leave():
        print("somebody disconnected")
socketio.run(app, host="0.0.0.0", port=80)
