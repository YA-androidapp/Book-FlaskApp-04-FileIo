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

@app.route('/write')
def write():
    text = 'foobar'
    resp = app.make_response(text)
    resp.mimetype = "text/plain"

    resp.set_cookie('username', 'the username')
    return resp
```

環境変数 `FLASK_APP` にファイル名を設定し、実行します。

```ps
C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> set FLASK_APP=app.py
(flaskenv) PS C:\Users\y\Documents\GitHub\Book-FlaskApp-04-FileIo> python -m flask run
```

ブラウザを開き、 [http://127.0.0.1:5000/write](http://127.0.0.1:5000/write) にアクセスしてから [http://127.0.0.1:5000/read](http://127.0.0.1:5000/read) にアクセスして、Cookie に書き込んだ `foobar` が表示されることを確認します。
