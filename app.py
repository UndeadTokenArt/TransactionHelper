from flask import Flask, render_template, request, flash
from main import word_replacer, get_docs_list, aquire_placeholders

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/result", methods=['GET', 'POST'])
def result():
    path = request.path
    working = True
    while working:
        for key, value in request.form.items():
            string = word_replacer(value, key, path)
            working = False
    return string

@app.route("/form", methods=['GET', 'POST'])
def returned_template():
    doc_list = get_docs_list()
    return render_template("form.html", doc_list=doc_list)


@app.route("/WR_step2", methods=['GET','POST'])
def wr_step2():
    path = f'documents/{request.form["path"]}'
    placeholders = aquire_placeholders(path)
    return render_template("WR_step2.html", placeholders=placeholders)
