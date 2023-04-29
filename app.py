from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from google.oauth2.credentials import Credentials
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/drive',
        'token_endpoint_auth_method': 'client_secret_post',
    },
)

@app.route("/")
def hello_world():
    email = session.get('profile')
    return render_template("index.html", email = email)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri, access_type='offline')

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token(access_type='offline')
    session['google_token'] = token

    # Retrieve the refresh token from the token response
    refresh_token = token.get('refresh_token')

    # Use the refresh token to create a Credentials object
    credentials = Credentials.from_authorized_user_info(
        session['google_token'],
        refresh_token=refresh_token,
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        token_uri='https://oauth2.googleapis.com/token'
    )

    resp = google.get('userinfo')
    session['profile'] = resp.json()
    return session['google_token']          # redirect(url_for('create_folder'))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



@app.route('/create_folder')
def create_folder():
    if 'google_token' not in session:
        return redirect(url_for('login'))

    # Load the user's credentials from the session
    credentials = Credentials.from_authorized_user_info(session['google_token'])

    try:
        # Use the Google Drive API to create a folder in the user's account
        service = build('drive', 'v3', credentials=credentials)
        folder_metadata = {'name': 'My Folder', 'mimeType': 'application/vnd.google-apps.folder'}
        folder = service.files().create(body=folder_metadata, fields='id').execute()

        return f'Folder created with ID: {folder.get("id")}'

    except HttpError as error:
        return f'An error occurred: {error}'


    return 'Folder created!'



'''
from flask import Flask, render_template, request, flash, url_for, redirect, session
from main import word_replacer, get_docs_list, aquire_placeholders, write_paired_list, check_for_match
from authlib.integrations.flask_client import OAuth
import markdown
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import flask_login

load_dotenv()  # take environment variables from .env.


# App config
app = Flask(__name__)
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file'},
)

# https://www.googleapis.com/auth/drive.file 
# https://www.googleapis.com/auth/drive



@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def hello_world():
    email = session.get('profile')
    return render_template("index.html", email = email)

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/new_client', methods=['GET'])
def create_folder():
    credentials = Credentials.from_authorized_user_info(requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json').json())
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
        'name': 'My Folder',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return f'Folder created with ID: {folder.get("id")}'




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


@app.route('/existing_client', methods=['GET'])
def existing_client():
    return render_template('existing_client.html')

@app.route('/tools', methods=['GET', 'POST'])
def tools(): 
    client_object_name = request.form['id']
    # details = my_client(client_object_name)
    # Calling to set up the client on the backend with the request form info
    # new_client_setup(request.form['id'])
    return render_template("tools.html", details=details)

'''