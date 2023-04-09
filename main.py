import re
import gspread
from google.oauth2.service_account import Credentials
import os
import ast

#this should be the way that we keep track of things in the transaction.
class Transaction:
    def __init__(self) -> None:
        self.__address = None
        self.__client = {
            'first_client_name': None, 
            'second_client_name': None,
            'third_client_name': None,
            'fourth_client_name': None
        }
        self.__inspection_days = {}
        self.__closing_date = None
        self.__rentback = None

        # get and set for address
        def get_address(self):
            return self.__address
        
        def set_address(self, address):
            self.__address = address
        
        #gets the client in the position of the dictionary, 
        def get_client(self, position):
            return self.__client[position] 
        
        def set_client(self, client, name):
            self.__client[client] = name

        # get and set for inspection days 
        def get_insp(self):
            return self.inspection_days
        
        def set_insp(self, start, length):
            self.__inspection_days[start] = start
            self.__inspection_days[length] = length

        #get and set for the expected closing day
        def get_closing(self):
            return self.__closing_date
        
        def set_closing(self, date):
            self.__closing_date = date

        #get and set for the rent back final day
        def get_rentback(self):
            return self.__rentback
        
        def set_rentback(self, date):
            self.__rentback = date


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
