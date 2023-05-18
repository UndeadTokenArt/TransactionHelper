from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv
from main import word_replacer, get_docs_list, aquire_placeholders, write_paired_list, check_for_match, client_list
import markdown

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
        'scope': 'profile'
    },
)

@app.route("/", methods=['GET','POST'])
def index():
    gprofile = session.get('profile')
    list = client_list()
    return render_template('index.html', client_list=list)


@app.route('/client_tools', methods=['GET','POST'])
def client_tools():
    if request.method == 'POST':
        client_name = request.form['client_name']
        new_string = client_name.replace(' ', '')
        dir_path = os.path.join('documents', new_string)
        os.makedirs(dir_path, exist_ok=True)
        return render_template("client_tools.html", client_name=new_string)
    else:
        return render_template('client_tools.html')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    session['google_token'] = {
        'access_token': token['access_token'],
        'scope' : token['scope'],
        'client_id' : os.getenv("GOOGLE_CLIENT_ID"),
        'client_secret' : os.getenv("GOOGLE_CLIENT_SECRET"),
        'refresh_token' : None
    }
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route("/WR_step1", methods=['GET', 'POST'])
def returned_template():
    client_name = request.form['client_name']
    my_dir = f'documents/{client_name}'
    doc_list = get_docs_list(client_name)
    return render_template("WR_step1.html", doc_list=doc_list, client_name=client_name, my_dir=my_dir)


@app.route("/WR_step2", methods=['GET','POST'])
def wr_step2():
    path = request.form["path"]
    # path = f'documents/{request.form["client_name"]}/{request.form["path"]}'
    filename, ext = os.path.splitext(path)
    placeholders = aquire_placeholders(path)
    dict_path = filename + '_Data' + ext
    if os.path.isfile(dict_path):
        placeholders = check_for_match(placeholders, dict_path)
    return render_template("WR_step2.html", placeholders=placeholders, path=path)


@app.route("/result", methods=['GET', 'POST'])
def result():
    path = request.form["client_name"]
    replacements = request.form.to_dict()
    write_paired_list(path, replacements)
    new_filename = word_replacer(replacements, path)
    with open(new_filename, "r") as f:
        display = markdown.markdown(f.read()) 
    
        #return display
        return render_template("result.html", display=display)

@app.route("/new_client", methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        new_client_folder = request.form['new_client_name']
        list = client_list(new_client_folder)
    return render_template('index.html', client_list=list)

@app.route('/add_doc', methods=['GET', 'POST'])
def add_doc():
        client_name = request.form['client_name']
        return render_template('add_doc.html', client_name=client_name)


@app.route('/upload_f', methods=['GET', 'POST'])
def add_file():
    if request.method == 'POST':
        # Get the uploaded file from the form
        file = request.files['upload_file']
        client_name = request.form['client_name']

        # Check if file is empty or not valid
        if file.filename == '':
            return render_template('add_doc', error='No file selected')
        if not allowed_file(file.filename):
            return render_template('/add_doc', error='Invalid file type')

        # Save the file to the documents directory
        file.save(os.path.join(f'documents/{client_name}', file.filename))

        # Redirect to the homepage or a success page
        return redirect('/client_tools')
    else:
        # If request method is GET, render the form page
        return render_template('/add_doc')


@app.route('/upload_t', methods=['GET', 'POST'])
def add_text():
    if request.method == 'POST':
        # Get the text from the form
        text = request.form['upload_ta']
        file_name = request.form['file_name']
        client_name = request.form['client_name']

        # Check if the text is not empty or invalid
        if not text:
            error = 'Please enter some text'
            return render_template('/add_doc', error=error)
        
        # save(os.path.join(f'documents/{client_name}', file.filename))
        
        # Save the text to a file
        with open(f'documents/{client_name}/{file_name}.txt', 'w') as f:
            f.write(text)

        # Redirect to the homepage or a success page
        return redirect('/')
    else:
        # If request method is GET, render the form page
        return render_template('/add_doc')

# Function to check if file type is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
