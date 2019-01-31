from flask import (Flask, render_template, session, 
                   redirect, url_for, escape, request)
from request_data import get_summoner, get_match_history
app = Flask(__name__)

# Set the secret key (session)
app.secret_key = b'_2#y5K"F7Q8x\n\xec]/'


@app.route("/")
def index(name=False):
    if session:
        name = session['username']
    return render_template('index.html', name=name)


@app.route('/profile')
def profile():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username']) + '<br> <a href="/">Home page</a>'
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('profile'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
# @app.route('/search/<name>')
def search_summoner():
    if request.method == 'POST':
        summoner_name = request.form['summoner']
        summoner = get_summoner(summoner_name, 'NA')
        matches = get_match_history(summoner['accountId'], 'NA')['matches']
        return render_template('index.html', summoner=summoner, matches=matches)
    return render_template('index.html')


# USE FLASK RUN INSTEAD/ export FLASK_APP=app.py / export FLASK_ENV=development / flask run
# if __name__ == '__main__':
#     app.run()