import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, send, emit

pictures = {}
connections = {}

ip = '192.168.1.6'
port = 3000
app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('connected')
def sock_connect():
    print(f'We have a connection {request.namespace.socket.sessid}')
    connections[request.namespace.socket] = 1


@app.route("/")
def home():
    print(request)
    return "Hello, world"


@app.route("/pic")
def pics():
    try:
        fname = request.args['name']
        return pictures[int(fname)]

    except FileNotFoundError or ValueError or KeyError:
        if not os.path.exists('1.jpg'):
            return send_file('error.png')
        else:
            return send_file('1.jpg')


@app.route("/upload", methods=["POST"])
def upload():
    print(request.data)
    print(list(request.headers.keys()))
    print(request.headers['Content-Disposition'])

    # filename will be like '1.jpeg'
    filename = request.headers['Content-Disposition']
    with open(filename, 'wb') as file:
        file.write(request.data)

    # get the number
    number = int(filename.split('.')[0])

    # store picture in memory
    pictures[number] = request.data
    return "OK!"


if __name__ == '__main__':
    app.run(host=ip, port=port, debug=True)