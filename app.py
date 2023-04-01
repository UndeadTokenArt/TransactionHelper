from flask import Flask, render_template, request, flash
from main import word_replacer, get_docs_list, aquire_placeholders

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/result", methods=['GET', 'POST'])
def result():
    path = f'documents/{request.form["path"]}'
    replacements = request.form.to_dict()
    
    # return request.form.to_dict()
    
    return word_replacer(replacements, path)

@app.route("/WR_step1", methods=['GET', 'POST'])
def returned_template():
    doc_list = get_docs_list()
    return render_template("WR_step1.html", doc_list=doc_list)


@app.route("/WR_step2", methods=['GET','POST'])
def wr_step2():
    passable = request.form["path"]
    path = f'documents/{request.form["path"]}'
    placeholders = aquire_placeholders(path)
    return render_template("WR_step2.html", placeholders=placeholders, passable=passable)
