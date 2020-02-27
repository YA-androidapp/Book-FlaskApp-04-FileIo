from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)
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
            <input type="text" name="username"><input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))