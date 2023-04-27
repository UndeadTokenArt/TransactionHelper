from flask import Flask, render_template, request, flash, url_for, redirect, session
from main import word_replacer, get_docs_list, aquire_placeholders, write_paired_list, check_for_match
from authlib.integrations.flask_client import OAuth
import markdown
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


load_dotenv()  # take environment variables from .env.


app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'


# oauth config
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
    client_kwargs={
    'scope': 'email profile https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/spreadsheets',
}
)

@app.route("/")
def hello_world():
    google_login_email = "Your Email here"
    return render_template("index.html", google_login_email=google_login_email)

@app.route('/login', methods=['GET'])
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scope
    user_info = resp.json()
    # user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/new_client', methods=['GET'])
def new_client():
    # Build the Drive API client
    credentials = session.get('authorization', None)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Set folder metadata
    folder_metadata = {
        'name': 'My new folder',
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # Create the folder
    try:
        folder = drive_service.files().create(body=folder_metadata).execute()
        print('Folder created: %s' % folder.get('webViewLink'))
    except HttpError as error:
        print('An error occurred: %s' % error)
    return render_template('new_client.html')




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

