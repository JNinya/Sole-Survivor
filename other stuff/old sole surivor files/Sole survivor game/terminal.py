#MADE BY JACK!!!!!!!!!!
#This modules handles everything involving the terminal
"""
Functions:

terminalInput(inputText)

Terminal Commands:
help

"""
from ioManager import *

error_message = "This command does not exist"

#parses whatever is put into it as a command and executes the function related to that command
def terminalInput(inputText):
    split_text = inputText.split()
    command = split_text[0]

    #without a parameter
    if len(split_text) == 1:
        try:
            eval(command.lower())()
        except:
            tPrint(error_message)
        else:
            eval(command.lower())()

    #with one parameter
    elif len(split_text) == 2:
        parameter1 = split_text[1]
        try:
            eval(command.lower())(parameter1)
        except:
            tPrint(error_message)
        else:
            eval(command.lower())(parameter1)

    #anything else
    else:
        tPrint(error_message)


#Everything below here is a terminal command. These should only be accessed locally through the terminalInput() function or other commands

def help():
    tPrint("This is the help text")


#debug/testing

terminalInput("this is not a command")
input()
terminalInput("help")
input()
terminalInput("help 50")
