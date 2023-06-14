import re
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
        

# opens a document in read mode
def opendoc(path):
    with open(path, "r") as f:
        return f.read()

# word replacement function, takes a dictionairy from a form and the path
def word_replacer(replacements, path, client_name):
    with open(path, 'r') as f:
        content = f.read()

    # Replace the words in the content using the replacements dictionary
    for key, value in replacements.items():
        content = content.replace(key, value)

    # Check if the file is from the base list and needs to have the path redirected to the client folder
    base_list = [f.name for f in os.scandir('documents/') if f.is_file()]
    my_filename = path[len('documents/'):]

    if my_filename in base_list:
        new_path = f'{path.rsplit("/", 1)[0]}/{client_name}/{path.rsplit("/", 1)[1]}'
        filename, ext = os.path.splitext(new_path)
        new_filename = filename + '_modified' + ext
    else:
        filename, ext = os.path.splitext(path)
        new_filename = filename + '_modified' + ext

    # Create the directory if it doesn't exist
    new_dir = f'{os.path.dirname(new_filename)}/modified'
    os.makedirs(new_dir, exist_ok=True)

    results = os.path.join(new_dir, os.path.basename(new_filename))

    # Write the modified content to the new file
    with open(results, 'w') as f:
        f.write(content)

    return results



# I want this fucntion to help get key and Value pairs
def get_values(form_data):
    return None



def write_paired_list(path, data, client_name):
    # Read the existing data from the file
    existing_data = []
    if os.path.isfile(path):
        with open(path, 'r') as f:
            existing_data = f.read().splitlines()

    # Extend the existing data with new data and remove duplicates
    updated_data = list(set(existing_data + data))

    # Create the directory if it doesn't exist
    new_dir = f'documents/{client_name}/data/'
    os.makedirs(new_dir, exist_ok=True)

    # Specify the file path
    my_dir = f'{new_dir}{client_name}.txt'

    # Write the updated data to the file
    with open(my_dir, 'w') as f:
        f.write('\n'.join(updated_data))

    return my_dir



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

# gathers the list of files inside the documents/{clients_name}/ directory and returns a list of the files
def get_docs_list(clients_name):
    folder_path = f'documents/{clients_name}/'
    base_path = 'documents/'
    doc_list = [f.name for f in os.scandir(folder_path) if f.is_file()]
    base_list = [f.name for f in os.scandir(base_path) if f.is_file()]
    doc_list.extend(base_list)
    return doc_list

# gets a list of the folders inside documents directory - the folders should have the name of a client
def client_list(new_dir = 'New Client'):
    folder_path = 'documents'
    folder_list = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    if new_dir != 'New Client':
        folder_list.append(new_dir)
    return folder_list



 # set each of the detail in details to their matching attrubute in the class transaction with the class being named after the value in the details list called Transactio_name
def set_client_details(details):
    for detail in details:
        return print(detail)
