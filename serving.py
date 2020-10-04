
import os

from flask import Flask, render_template, request, jsonify, send_file

ip = '192.168.1.6'
port = 3000
app = Flask(__name__)


@app.route("/")
def home():
    print(request)
    return "Hello, world"


@app.route("/pic")
def pics():

    try:

        fname = request.args['name']
        return send_file(fname)

    except FileNotFoundError or ValueError or KeyError:
        if not os.path.exists('cam1.jpg'):
            return send_file('error.png')
        else:
            return send_file('cam1.jpg')






@app.route("/upload", methods=["POST"])
def upload():
    print(request.data)
    print(list(request.headers.keys()))
    print(request.headers['Content-Disposition'])
    with open(request.headers['Content-Disposition'], 'wb') as file:
        file.write(request.data)
    return "OK!"



if __name__ == '__main__':
    app.run(host=ip, port=port, debug=True)