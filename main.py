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

# word replacement function, takes word to replace with, placeholder to change and path of document
def word_replacer(arg1, arg2, path):
        doc = opendoc(path)
        words = doc.split()
        
        
        for i in range(len(words)):
            if words[i] == arg2:
                words[i] = arg1


        return " ".join(words)

# finds a placeholder word in a string and returns a list of all words found
def aquire_placeholders(path):
    doc = opendoc(path)
    return set(re.findall(r'\[[^\]]*\]', doc))


def get_docs_list():
    folder_path = 'documents'
    doc_list = [f.name for f in os.scandir(folder_path) if f.is_file()]
    return doc_list


# get a list of all the text files in the format folder
# make a dictionary that holds a value for replacing words and what words are being replaced.