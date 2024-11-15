# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import base64

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/stream')
# def stream():
#     return render_template('stream.html')

# @app.route('/view')
# def view():
#     return render_template('view.html')

# @socketio.on('stream')
# def handle_stream(data):
#     emit('stream_data', data, broadcast=True, include_self=False)

# @socketio.on('capture')
# def handle_capture(data):
#     emit('captured_image', data, broadcast=True)

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('stream')
def handle_stream(data):
    emit('stream_data', data, broadcast=True, include_self=False)

@socketio.on('capture')
def handle_capture(data):
    emit('captured_image', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)