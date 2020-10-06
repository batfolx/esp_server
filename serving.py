import os
from flask import Flask, render_template, request, jsonify, send_file, session, copy_current_request_context
from flask_socketio import SocketIO, send, emit

login = 'XXXXXXXX'
password = 'XXXXXXXX'

pictures = {}

ip = '192.168.1.6'
port = 3000
app = Flask(__name__)

socketio = SocketIO(app)


@socketio.on("camera")
def handle_camera(data):
    try:
        camnum = int(data['cam'])
    except Exception:
        camnum = 1

    _login = data['login']
    _password = data['password']

    if login == _login and _password == password:
        emit('data', {
            'data': pictures[camnum]
        })
    else:
        emit('data', {
            'data': 0
        })


@app.route("/")
def home():
    print(request)
    return "Hello, world"


@app.route("/auth", methods=['GET'])
def auth():
    try:
        _login = request.headers['Login']
        _password = request.headers['Password']


        if _login == login and _password == password:
            print("Valid!")
            return jsonify({
                'error': ''
            })
        else:
            print("INVALID")
            return jsonify({
                'error': 'invalid'
            })

    except:
        return jsonify({
            'error': 'invalid',
        })


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
   # print(request.data)
   # print(list(request.headers.keys()))
   # print(request.headers['Content-Disposition'])

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



    socketio.run(app, host=ip, port=port, debug=True)

