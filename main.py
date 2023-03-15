import re


# opens a document in read mode
def opendoc(path):
    with open(path, "r") as f:
        return f.read()

# word replacement function, takes word to replace with, placeholder to change and path of document
def word_replacer(key, placeholder, path):
        doc = opendoc(path)
        words = doc.split()
        for i in range(len(words)):
            if words[i] == placeholder:
                words[i] = key
        return " ".join(words)

# finds a placeholder word in a string and returns a list of all words found
def lookup(path):
    doc = opendoc(path)
    return re.findall(r'\[[^\]]*\]', doc)


print(lookup("template.txt"))
             


#function that looks through a document or folder and gets all placeholders
#function that makes a list of placeholder words and make sure there are no duplicates
#function that makes a spread sheet that will have placeholders in one column
#function that saves the document
#function that combines first and last names into one string
#function that connects to google drive?????
#function that prompts for matching the replacment word with the placeholder
#function that asks if there are more than one set of names to be used in the contract
