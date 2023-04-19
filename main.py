import re
import gspread
from google.oauth2.service_account import Credentials
import os
import ast


#this should be the way that we keep track of things in the transaction.
class Transaction:
    def __init__(self) -> None:
        self.id = None
        self.address = None
        self.client = {
            'first_client_name': None, 
            'second_client_name': None,
            'third_client_name': None,
            'fourth_client_name': None
        }
        self.email = None,
        self.phone =[]
        self.inspection_days = {}
        self.closing_date = None
        self.rentback = None
        self.directory = None # Initialize here

def my_client(client_object_name):
    client_object_name = Transaction
    attrs = dir(client_object_name)
    for attr in attrs:    
        client_object_name.attr = request.form[f'{attr}']



# this fucntion doesn't actually do anything yet, just the idea of what I want it to do.
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
    new_filename = filename + '_modified' + ext

    # Write the modified content to the new file
    with open(new_filename, 'w') as f:
        f.write(content)

    return new_filename

# I want this fucntion to help get key and Value pairs
def get_values(form_data):
    return None



# Function should save a document, and return the path and filename
def write_paired_list(path, data):
    filename, ext = os.path.splitext(path)
    new_filename = filename + '_Data' + ext

    # Write the modified content to the new file
    with open(new_filename, 'w') as f:
        f.write(str(data))
    return new_filename


# finds a placeholder word in a string and returns a list of all words found
def aquire_placeholders(path):
    doc = opendoc(path)
    pattern = r'\[[^\]]*\]'
    my_list = list(set(re.findall(pattern, doc)))
    my_list.sort()
    
    return my_list
    # return set(re.findall(pattern, doc))


# checks a dictionairy for a match in a list. returns the a new_dictionairy with only matching keys to the list
def check_for_match(my_list, dict_path):
    my_dict = ast.literal_eval(opendoc(dict_path))
    new_dict = {}
    for key, value in my_dict.items(): 
        if key in my_list:
            new_dict[key] = value
    return new_dict


def get_docs_list():
    folder_path = 'documents'
    doc_list = [f.name for f in os.scandir(folder_path) if f.is_file()]
    return doc_list

 # set each of the detail in details to their matching attrubute in the class transaction with the class being named after the value in the details list called Transactio_name
def set_client_details(details):
    for detail in details:
        return print(detail)

def import_drive_docs(folder_id, credentials):
    credentials = service_account.Credentials.from_service


#testing for functionality


'''
billz = Transaction()
billz.set_address('14825 SE 119th Clackamas OR')
billz.set_client('first_client_name', 'Stephen Moore')
print(billz.get_client('first_client_name'))
'''


