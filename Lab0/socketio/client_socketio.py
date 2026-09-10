import socketio

sio = socketio.Client()

@sio.event
def connect():
    print(' connection established')

@sio.event
def disconnect():
    print(' disconnected from server')

sio.connect('http://localhost:8080')

sio.emit('message', 'I am Kuangda, I am sad.')

input('Enter to dc...')
sio.disconnect()
