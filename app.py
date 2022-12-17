from flask import Flask, render_template, request, redirect, escape, session, flash
from flask_session import Session
from markupsafe import escape
from search4web import search4letters, log_request
from baseDatos import log_request_bd, readlog_bd, register_bd, login_bd, check_token, get_stats

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
                           the_title='Search for letters',
                           the_username=session.get('name'))


@app.route("/")
@app.route("/index")
def index_page() -> 'html':
    return render_template('index.html',
                           the_title='Welcome to search for letters on the web!')


@app.route("/login", methods=['POST'])
def login_page() -> 'html':
    action = request.form['action']
    if action == 'Register':
        if register_bd(request):
            return render_template('login.html',
                                    the_title=action)
        else:
            flash('Usuario ya registrado.')
            return redirect('/', code=302)
    elif action == 'Login':
        token = login_bd(request)
        if token != 'Error':
            session["name"] = request.form['usuario']
            session['token'] = token
            return redirect("/entry", code=302)
        else:
            return redirect("/", code=302)
    elif action == 'Anonymous':
        session["name"] = 'Anonymous'
        return redirect("/entry", code=302)


@app.route("/logout")
def logout():
    session["name"] = None
    session["token"] = None
    return redirect("/")


@app.route("/stats")
def stats():
    rankingGeneral, rankingPropio = get_stats(session.get('name'))
    return render_template('stats.html',
                           the_title='Words Rankings',
                           Gword1=rankingGeneral[0][0],
                           Gword2=rankingGeneral[0][1],
                           Gword3=rankingGeneral[0][2],
                           Gword1count=rankingGeneral[1][0],
                           Gword2count=rankingGeneral[1][1],
                           Gword3count=rankingGeneral[1][2],
                           Gword1per=rankingGeneral[2][0],
                           Gword2per=rankingGeneral[2][1],
                           Gword3per=rankingGeneral[2][2],
                           Uword1=rankingPropio[0][0],
                           Uword2=rankingPropio[0][1],
                           Uword3=rankingPropio[0][2],
                           Uword1count=rankingPropio[1][0],
                           Uword2count=rankingPropio[1][1],
                           Uword3count=rankingPropio[1][2],
                           Uword1per=rankingPropio[2][0],
                           Uword2per=rankingPropio[2][1],
                           Uword3per=rankingPropio[2][2],
                           )


@app.route("/result", methods=['POST'])
def results_page():
    title = "Here are your results"
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    check = check_token(session.get("name"), session.get("token"))
    if check:
        log_request_bd(session.get('name'), request, results)
    else:
        log_request_bd('Anonymous', request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)


@app.route('/viewlog')
def view_the_log() -> str:
    contents = readlog_bd()
    return escape(contents)
