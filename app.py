from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

@app.route('/parse/json', methods=['GET', 'POST', 'DELETE', 'PUT'])
def add():
    if request.headers.get("Content-Type") == 'application/json':
        # HTTPリクエストのMIMEタイプがapplication/json
        data = request.get_json()
        return jsonify(data)
    else:
        json_message = {
            'error':'Not supported: {}'.format(request.headers.get("Content-Type"))
        }
        return make_response(jsonify(json_message), 400)
