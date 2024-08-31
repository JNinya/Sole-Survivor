"""
Functions:

read(filename)

write(filename, text)

"""

# Returns the text of a text file
def read(filename):
    file = open(filename, "r")
    output = file.read()
    file.close()
    return output

# Overwrites the text of a text file. Creates a new file if one doesn't exist
def write(filename, text):
    file = open(filename, "w")
    output = file.write(text)
    file.close()
    return output
