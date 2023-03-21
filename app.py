from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<button type='button'>User</button> <button>Find All</button> <button>Build</button>"