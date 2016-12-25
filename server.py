from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import eventlet
from random import choice
import sqlite3
conn = sqlite3.connect('chatRoom.db')
c = conn.cursor()
#run these lines only if you want to create a new database
#c.execute("CREATE TABLE rooms (name TEXT);")
#conn.commit()

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

@app.route('/chat/<roomID>/')
def room(roomID):
	return render_template('index.html',room=roomID)

#homepage sends a POST request, returns a new room
@app.route('/create', methods = ['POST'])
def create_room():
	#list of all alphanumeric characters
	chars = [chr(a) for a in (range(48,58)+range(97,123)+range(65,91))]
	while True:
		#generate chat room name
		roomName = "".join([choice(chars) for a in range(8)])
		c.execute("SELECT * FROM ChatRooms WHERE name=\""+roomID+"\"")
		if c.fetchall():
			c.execute("INSERT INTO rooms VALUES (\""+roomID+"\")")
			conn.commit()
			return roomID

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
