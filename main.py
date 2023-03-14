def word_replacer(key, placeholder, document):
    with open(document, "r") as f:
        doc = f.read()
    words = doc.split()
    for i in range(len(words)):
        if words[i] == placeholder:
            words[i] = key
    return " ".join(words)


print(word_replacer("Stephen","[[First_Name]]", "template.txt"))