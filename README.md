# Book-FlaskApp-04-FileIo

---

## Flask のインストール

仮想環境を用意して、Flask パッケージを(ローカル)インストールします。

```ps
PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> py -m venv flaskenv
PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> flaskenv\Scripts\activate
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> py -m pip install Flask
```

## Cookie を読み書きする

[app.py](app.py) を作成し、以下のコードを書きます。 [app01.py](app01.py)

```py
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

```

環境変数 `FLASK_APP` にファイル名を設定し、実行します。

```ps
C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> set FLASK_APP=app.py
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
```

ブラウザを開き、 [http://127.0.0.1:5000/write](http://127.0.0.1:5000/write) にアクセスしてから [http://127.0.0.1:5000/read](http://127.0.0.1:5000/read) にアクセスして、Cookie に書き込んだ `foobar` が表示されることを確認します。

## Session を読み書きする

Session を利用するにあたって、シークレットキーが必要になるので、ランダムなバイト列を生成します。

```ps
PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> py -c 'import os; print(os.urandom(16))'
b'K\x93\x9fj\xe9\r\x13\xad\xe1\x041\xcc\xf9\x8e\x00\xfb'
```

```ps
PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> py
>>> import os
>>> os.urandom(16)
b'K\x93\x9fj\xe9\r\x13\xad\xe1\x041\xcc\xf9\x8e\x00\xfb'
>>>
```

[app.py](app.py) を以下のコードに置き換えます。 [app02.py](app02.py)

```py
from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'K\x93\x9fj\xe9\r\x13\xad\xe1\x041\xcc\xf9\x8e\x00\xfb'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s<br><a href="%s">Log out</a>' % (escape(session['username']), url_for('logout'))
    return 'You are not logged in<br><a href="%s">Log in</a>' % url_for('login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <input type=text name=username><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
```

環境変数 `FLASK_APP` にファイル名を設定し、実行します。

```ps
C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> set FLASK_APP=app.py
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
```

ブラウザを開き、 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) にアクセスして、ログイン・ログアウトできることを確認します。

## JSON を受け取ったり、返したりする

[app.py](app.py) を以下のコードに置き換えます。 [app03.py](app03.py)

```py
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
```

環境変数 `FLASK_APP` にファイル名を設定し、実行します。

```ps
C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> set FLASK_APP=app.py
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
```

(RESTED などの)REST クライアントを開き、 [http://127.0.0.1:5000/parse/json](http://127.0.0.1:5000/parse/json) に JSON 形式のリクエストボディを送信して、送ったデータと同じ JSON 形式のレスポンスボディになっていることを確認します。
また、MIME タイプを変更するとエラーメッセージが返ることを確認します。

<img src="README-src/rested01.png" width="30%" alt="成功時" />
<img src="README-src/rested02.png" width="30%" alt="エラー時" />

## ログを保存する

[app.py](app.py) を以下のコードに置き換えます。 [app04.py](app04.py)

```py
from flask import Flask, make_response

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return make_response('logging', 400)
```

環境変数 `FLASK_APP` にファイル名を設定し、実行します。

```ps
C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> set FLASK_APP=app.py
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
```

(RESTED などの)REST クライアントを開き、 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) にアクセスした後、ターミナルに以下のようにログが出力されていることを確認します。

```ps
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
[2020-02-27 12:17:30,865] WARNING in app: A warning occurred (42 apples)
[2020-02-27 12:17:30,866] ERROR in app: An error occurred
127.0.0.1 - - [27/Feb/2020 12:17:30] "GET / HTTP/1.1" 400 -
```

デフォルトでは、ログレベルが `WARN` 以上のものしか出力されないので、 `INFO` なども出力させたい場合は以下のコードを追記します。

```py
# app = Flask(__name__) の次の行の辺りに追記

app.logger.setLevel(logging.DEBUG)
```

```ps
[2020-02-27 12:25:45,029] DEBUG in app: A value for debugging
[2020-02-27 12:25:45,030] WARNING in app: A warning occurred (42 apples)
[2020-02-27 12:25:45,031] ERROR in app: An error occurred
127.0.0.1 - - [27/Feb/2020 12:25:45] "GET / HTTP/1.1" 400 -
```

ファイルにも書き出す場合は以下のコードを追記します。 `app.logger.setLevel` に指定したログレベルの方が、 `fileHandler.setLevel` で指定したログレベルよりも優先されます。

```py
# app = Flask(__name__)

# app.logger.setLevel(logging.DEBUG) の次の行の辺りに追記

LOGFILE = 'app.log'
LOGFORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
fileHandler = logging.FileHandler(LOGFILE)
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGFORMAT)
fileHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
```

## ファイルをアップロードする

`enctype=multipart/form-data` 属性が指定された `form` の中にある `input type="file" />` タグで選択されたファイルを受け取ります。

`secure_filename()` 関数を使用してファイル名に含まれると問題のある文字列を除去してから、 `file.save()` 関数を利用して保存します（本来はユーザーから受け取ったファイル名を使用するのではなく、サーバー側で生成するべきです）。

[app.py](app.py) を以下のコードに置き換えます。 [app05.py](app05.py)

```py
import os
from flask import Flask, flash, make_response, redirect, request, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input type="submit" value="Upload" />
    </form>
    '''

@app.route('/uploaded_file')
def uploaded_file():
    filename = request.args.get('filename', '')
    resp = app.make_response('Uploaded: {}'.format(filename))
    resp.mimetype = "text/plain"
    return resp
```

環境変数 `FLASK_APP` にファイル名を設定し、実行します。

```ps
C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> set FLASK_APP=app.py
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
```

ブラウザを開き、 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) にアクセスした後、任意のファイルを選択してアップロードできることを確認します。

※このサンプルは安全ではないので、実稼働環境では使用しないでください。
