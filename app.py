from flask import Flask, render_template, request, redirect,escape
from markupsafe import escape
from search4web import search4letters,log_request

app = Flask(__name__)


#@app.route("/")
#def hello() -> '302':
#    return redirect('/entry')


@app.route("/search", methods=['POST'])
def search():
    return str(search4letters(request.form['phrase'], request.form['letters']))


@app.route("/")
@app.route("/entry")
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search for letters on the web!')


@app.route("/result", methods=['POST'])
def results_page():
    title = "Here are your results"
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    log_request(request,results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)

@app.route('/viewlog')
def view_the_log() -> str:
    with open('vsearch.log','r') as log:
        contents = log.read()
    return escape(contents)
