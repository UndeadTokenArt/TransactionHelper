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
    return set(re.findall(r'\[[^\]]*\]', doc))
