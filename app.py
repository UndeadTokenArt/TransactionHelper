from flask import Flask, render_template, request, flash
from main import word_replacer

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/result/<key>", methods=['POST', 'GET'])
def test(key):
    text = word_replacer(key)
    return f"<p>{text}</p>"

@app.route("/textreplacer")
def textreplacer():
    return render_template("form.html")