"""
Functions:

read(filename)

write(filename, text)

"""

# Returns the text of a text file
def read(file_name):
    file = open(file_name, "r", encoding="utf8")
    output = file.read()
    file.close()
    return output

# Overwrites the text of a text file. Creates a new file if one doesn't exist
def write(file_name, text):
    file = open(file_name, "w", encoding="utf8")
    output = file.write(text)
    file.close()
    return output
