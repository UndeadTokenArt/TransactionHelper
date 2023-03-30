from flask import Flask, render_template, request, flash
from main import word_replacer, get_docs_list, aquire_placeholders

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
        return render_template('index.html')

@app.route("/form", methods=['GET', 'POST'])
def returned_template():
    doc_list = get_docs_list()
    return render_template("form.html", doc_list=doc_list)


@app.route("/WR_step2", methods=['GET','POST'])
def wr_step2():
    placeholders = aquire_placeholders('documents/template.txt')
    return render_template("WR_step2.html", placeholders=placeholders)
