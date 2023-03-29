from flask import Flask, render_template, request, flash
from main import word_replacer

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        arg1 = request.form['arg1']
        arg2 = request.form['arg2']
        return word_replacer(arg1, arg2)
    else:
        return render_template('not_found.html')

@app.route("/form")
def returned_template():
    return render_template("form.html")