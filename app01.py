from flask import Flask, make_response, request

app = Flask(__name__)


@app.route('/read')
def read():
    username = request.cookies.get('username', 'NOT_FOUND')

    resp = app.make_response(username)
    resp.mimetype = "text/plain"
    return resp


@app.route('/write')
def write():
    text = 'foobar'
    resp = app.make_response(text)
    resp.mimetype = "text/plain"

    resp.set_cookie('username', text)
    return resp
