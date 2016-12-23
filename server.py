from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
global id
id=0
@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('msg')
def handle_msg(msg):
	#Messages are in the form ROOM:::MESSAGE
	print('received' + msg)
	emit('receive', msg, room=msg.split(":::")[0])

@socketio.on('join')
def on_join(room):
	global id
	id+=1
	join_room(room)
	print(room)
	#emit('confirm', str(id))
	emit('receive', 'User'+str(id)+'has entered the room.', room=room)


@socketio.on('leave')
def on_leave(room):
	leave_room(room)
	send('memer has left the room.', room=room)
