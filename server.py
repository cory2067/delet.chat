from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import eventlet

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
