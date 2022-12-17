from flask import Flask, render_template, request, redirect, escape
from markupsafe import escape
from search4web import search4letters, log_request
from baseDatos import log_request_bd, readlog_bd, register_bd, login_bd

app = Flask(__name__)


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
        login_bd(request)
        return redirect("/entry", code=302)
    elif action == 'Anonymous':
        return redirect("/entry", code=302)


@app.route("/result", methods=['POST'])
def results_page():
    title = "Here are your results"
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    log_request_bd(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)


@app.route('/viewlog')
def view_the_log() -> str:
    contents = readlog_bd()
    return escape(contents)
