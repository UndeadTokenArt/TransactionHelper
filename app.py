from flask import Flask, render_template, request, flash
from main import word_replacer, get_docs_list, aquire_placeholders, write_paired_list, check_for_match
import markdown
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/result", methods=['GET', 'POST'])
def result():
    path = f'documents/{request.form["path"]}'
    replacements = request.form.to_dict()
    write_paired_list(path, replacements)
    new_filename = word_replacer(replacements, path)
    with open(new_filename, "r") as f:
        display = markdown.markdown(f.read()) 
    
        #return display
        return render_template("result.html", display=display)

@app.route("/WR_step1", methods=['GET', 'POST'])
def returned_template():
    doc_list = get_docs_list()
    return render_template("WR_step1.html", doc_list=doc_list)


@app.route("/WR_step2", methods=['GET','POST'])
def wr_step2():
    passable = request.form["path"]
    path = f'documents/{request.form["path"]}'
    filename, ext = os.path.splitext(path)
    placeholders = aquire_placeholders(path)
    dict_path = filename + '_Data' + ext
    if os.path.isfile(dict_path):
        placeholders = check_for_match(placeholders, dict_path)
    
    return render_template("WR_step2.html", placeholders=placeholders, passable=passable)
