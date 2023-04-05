import re
import gspread
from google.oauth2.service_account import Credentials
import os

'''
Code used for connecting the google account Oauth stuff _ not ready yet 


# Load credentials from the JSON key file
creds = Credentials.from_service_account_file('path/to/key.json')

# Authenticate with gspread
client = gspread.authorize(creds)

# Open the spreadsheet by name
sheet = client.open('Spreadsheet Name').sheet1
'''

def start_gspread():
    gc = gspread.service_account()
    try:
        wks = gc.open("WordReplacemenmt").sheet1
    except:
        gc.create('WordReplacemenmt')
        raise Exception("No sheet found, new one created")
        

# opens a document in read mode
def opendoc(path):
    with open(path, "r") as f:
        return f.read()

# word replacement function, takes a dictionairy from a form and the path
def word_replacer(replacements, path):
    with open(path, 'r') as f:
        content = f.read()

    # Replace the words in the content using the replacements dictionary
    for key, value in replacements.items():
        content = content.replace(key, value)

    # Create a new filename for the modified file
    filename, ext = os.path.splitext(path)
    new_filename = "modified/" + filename + '_modified' + ext

    # Write the modified content to the new file
    with open(new_filename, 'w') as f:
        f.write(content)

    return new_filename

# finds a placeholder word in a string and returns a list of all words found
def aquire_placeholders(path):
    doc = opendoc(path)
    pattern = r'\[[^\]]*\]'
    my_list = list(set(re.findall(pattern, doc)))
    my_list.sort()
    
    return my_list
    # return set(re.findall(pattern, doc))


def get_docs_list():
    folder_path = 'documents'
    doc_list = [f.name for f in os.scandir(folder_path) if f.is_file()]
    return doc_list

print(aquire_placeholders("documents/template.md"))