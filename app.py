from flask import Flask, render_template, request, redirect, escape, session
from flask_session import Session
from markupsafe import escape
from search4web import search4letters, log_request
from baseDatos import log_request_bd, readlog_bd, register_bd, login_bd, check_token

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/search", methods=['POST'])
def search():
    return str(search4letters(request.form['phrase'], request.form['letters']))


@app.route("/entry")
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search for letters on the web!')


@app.route("/")
@app.route("/index")
def index_page() -> 'html':
    return render_template('index.html',
                           the_title='Welcome to search for letters on the web!')


@app.route("/login", methods=['POST'])
def login_page() -> 'html':
    action = request.form['action']
    if action == 'Register':
        register_bd(request)
        return render_template('login.html',
                               the_title=action)
    elif action == 'Login':
        token = login_bd(request)
        if token != 'Error':
            session["name"] = request.form['usuario']
            #session['token'] = token
            return redirect("/entry", code=302)
        else:
            return redirect("/", code=302)
    elif action == 'Anonymous':
        return redirect("/entry", code=302)


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/stats")
def stats():
    return render_template('stats.html')


@app.route("/result", methods=['POST'])
def results_page():
    title = "Here are your results"
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    #check = check_token(session.get("token"), request)
    log_request_bd(session.get('name'), request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)


@app.route('/viewlog')
def view_the_log() -> str:
    contents = readlog_bd()
    return escape(contents)
