"""
Change the color of printed text
"""

def red(text):
    return f"\u001b[31m{text}\u001b[0m"

def green(text):
    return f"\u001b[32m{text}\u001b[0m"

def yellow(text):
    return f"\u001b[33m{text}\u001b[0m"

def blue(text):
    return f"\u001b[34m{text}\u001b[0m"

def magenta(text):
    return f"\u001b[35m{text}\u001b[0m"

def cyan(text):
    return f"\u001b[36m{text}\u001b[0m"

def white(text):
    return f"\u001b[37m{text}\u001b[0m"

def lightRed(text):
    return f"\u001b[31;1m{text}\u001b[0m"

def lightGreen(text):
    return f"\u001b[32;1m{text}\u001b[0m"

def lightYellow(text):
    return f"\u001b[33;1m{text}\u001b[0m"

def lightBlue(text):
    return f"\u001b[34;1m{text}\u001b[0m"

def lightMagenta(text):
    return f"\u001b[35;1m{text}\u001b[0m"

def lightCyan(text):
    return f"\u001b[36;1m{text}\u001b[0m"

def lightWhite(text):
    return f"\u001b[37;1m{text}\u001b[0m"

"""MEssing around with in-line color codes:
def color(text):
    splitText = text.split("[")
    for i in range(len(splitText)):
        splitText[i] = splitText[i].split("]")
    print(splitText)
"""

accepted_colors = [
    "[red]",
    "[green]",
    "[yellow]",
    "[blue]"
]

def color(text):
    for i in accepted_colors:
        if text.find(i) != -1:
            print("color code found")
        