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

opening_color_codes = [
    "[red]",
    "[green]",
    "[yellow]",
    "[blue]"
]

closing_color_codes = [
    "[/red]",
    "[/green]",
    "[/yellow]",
    "[/blue]"
]

#Input text with inline custom color codes and output ANSI color codes
def color(text):
    actual_text = text
    for i in range(len(opening_color_codes)):
        current_color_code = opening_color_codes[i]
        if actual_text.find(current_color_code) != -1:
            #print("opening color code found")
            divided_string = actual_text.split(current_color_code)
            #print(divided_string)
            #print(i)
            second_half_of_string = divided_string[1]
            #print(second_half_of_string)
            #print(second_half_of_string.find(closing_color_codes[i]))
            second_half_of_string = second_half_of_string.split(closing_color_codes[i])
            #print(second_half_of_string)
            divided_string.pop()
            divided_string.append(second_half_of_string[0])
            divided_string.append(second_half_of_string[1])
            #print(divided_string)
            divided_string[1] = eval(getColorFromColorCode(current_color_code))(divided_string[1])
            #print(divided_string)
            final_string = divided_string[0] + divided_string[1] + divided_string [2]
            actual_text = final_string
    return actual_text



def getColorFromColorCode(code):
    code = code.split("[")
    code = code[1]
    code = code.split("]")
    code = code[0]
    return code




#debug/testing

test_text1 = "This is test text to check the [yellow]color of printed[/yellow] text. This is a second [red]color[/red] code"
test_text2 = "[yellow]This is test text to check the [green]color[/green] of printed text. This is a second [red]color[/red] code[/yellow]"

print(color(test_text1))
print(color(test_text2))
