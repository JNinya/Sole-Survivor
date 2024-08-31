#CODED BY JACK WOOOO
"""
Functions:

rPrint(text)

tPrint(text)

getUserInput()

"""

import os

#print for regular text
#this is the one to use for printing anytime you aren't in the terminal in game
def rPrint(text):
    os.system('cls')
    print(text)

#print for in game terminal output
#might add animations later in this function
def tPrint(text):
    os.system('cls')
    print(text.upper())

#requests user input and returns it as a string
def getUserInput():
    inputText = input()
    return inputText