from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import eventlet
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = dict()

@app.route('/')
def index():
	return render_template('newhomepage.html')

@app.route('/<roomID>')
def room(roomID):
	return render_template('chat.html', room=roomID)

#homepage sends a POST request, returns a new room
@app.route('/create', methods = ['POST'])
def create_room():
	#list of all alphanumeric characters
	chars = [chr(a) for a in (list(range(48,58))+list(range(97,123))+list(range(65,91)))]
	roomID = "".join([choice(chars) for a in range(8)])
	rooms[roomID] = []
	print('inner rooms var: ' + str(rooms))
	return roomID


@socketio.on('send')
def handle_msg(data):
		#Messages are in the form ROOM:::MESSAGE
		emit('display', data, room=data['room'])
		eventlet.sleep(0)

@socketio.on('join')
def on_join(data):
		room = data['room']
		print(data)
		if room not in rooms:
			rooms[room] = []
		rooms[room].append(data['name'])
		join_room(room)
		print("user joined room:" + room)
		print('rooms var in on join: ' + str(rooms))
		#emit('confirm', str(id))
		emit('display', {'name': 'sys', 'msg': data['name'] + ' has entered the room.'}, room=room)
		emit('listusers', {'users': rooms[room]}, room=room)
		eventlet.sleep(0)


@socketio.on('leave')
def on_leave(data):
	username = data['name']
	room = data['room']
	rooms[room].remove(username)
	emit('listusers', {'users': rooms[room]}, room=room)
	emit('display', {'name': 'sys', 'msg': username + ' left.'}, room=room)
	print(username + " disconnected from room " + room)

socketio.run(app, host="127.0.0.1", port=5000) #for testing
