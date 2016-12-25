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
	return render_template('homepage.html')

@app.route('/<roomID>')
def room(roomID):
	return render_template('chatroom.html',room=roomID)

#homepage sends a POST request, returns a new room
@app.route('/create', methods = ['POST'])
def create_room():
	#list of all alphanumeric characters
	chars = [chr(a) for a in (list(range(48,58))+list(range(97,123))+list(range(65,91)))]
	while True:
		#generate chat room name
		roomID = "".join([choice(chars) for a in range(8)])
		c.execute("SELECT * FROM rooms WHERE name=\""+roomID+"\"")
		if not c.fetchall():
			c.execute("INSERT INTO rooms VALUES (\""+roomID+"\")")
			conn.commit()
			return roomID


@socketio.on('send')
def handle_msg(data):
        #Messages are in the form ROOM:::MESSAGE
        emit('display', data, room=data['room'])
        eventlet.sleep(0)

@socketio.on('join')
def on_join(room):
        global id
        id+=1
        join_room(room)
        print(room)
        #emit('confirm', str(id))
        emit('display', {'name': 'sys', 'msg': 'User '+str(id)+' has entered the room.'}, room=room)
        eventlet.sleep(0)

@socketio.on('disconnect')
def on_leave():
        print("somebody disconnected")
socketio.run(app, host="0.0.0.0", port=80)
#socketio.run(app, host="127.0.0.1", port=5000) #for testing
