"""
Change the color of printed text
"""

from collections import deque
from enum import Enum

class ColorCode(Enum):
    CLEAR   = "\033[0m",

    RED     = "\033[31m",
    GREEN   = "\033[32m",
    YELLOW  = "\033[33m",
    BLUE    = "\033[34m",
    MAGENTA = "\033[35m",
    CYAN    = "\033[36m",
    WHITE   = "\033[37m",
    LIGHT_RED     = "\033[31;1m",
    LIGHT_GREEN   = "\033[32;1m",
    LIGHT_YELLOW  = "\033[33;1m",
    LIGHT_BLUE    = "\033[34;1m",
    LIGHT_MAGENTA = "\033[35;1m",
    LIGHT_CYAN    = "\033[36;1m",
    LIGHT_WHITE   = "\033[37;1m",

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

"""Messing around with in-line color codes:
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
            divided_string[1] = eval(getColorFromColorTag(current_color_code))(divided_string[1])
            #print(divided_string)
            final_string = divided_string[0] + divided_string[1] + divided_string [2]
            actual_text = final_string
    return actual_text


# use stack to keep track of colors
# read string linearly
# when encountering open tag, push new color and replace with color code
# when encountering close tag, pop color and apply top-of-stack color code (white if empty)

# TODO: update color codes with styles and other customizations
def gabeColor(text: str, default_color: ColorCode = ColorCode.WHITE):
    text_list: list[str] = [] # recompile text after replacing color codes
    color_stack = deque()
    text_begin = 0
    tag_begin = 0
    tag_end = 0
    while (tag_begin := text.find('|', tag_end)) != -1:
        tag_end = text.find('|', tag_begin + 1)
        tag = text[tag_begin:tag_end+1]
        
        #print(f"text_begin: {text_begin}, tag_begin: {tag_begin}, tag_end: {tag_end}")
        #print(tag)
        
        color_enum = default_color
        if not isClosingColorTag(tag):    
            color = getColorFromColorTag(tag)
            color_enum = ColorCode[color.upper()]
            color_stack.append(color_enum)
        else:
            color_stack.pop()
            color_enum = color_stack[-1] if len(color_stack) > 0 else default_color

        text_list.append(text[text_begin:tag_begin])
        text_list.append(color_enum.value[0])

        tag_end += 1
        text_begin = tag_end

    text_list.append(text[text_begin:]) # append rest of text after final tag
    compiled_text = "".join(text_list)
    print(compiled_text)


def getColorFromColorTag(tag: str) -> str: # example: |yellow| or |/yellow|
    first_char = 1 if tag[1] != '/' else 2
    color = tag[first_char:-1]
    return color

def isClosingColorTag(tag: str) -> bool:
    # efficient because left side is faster, but right side guarentees tag can find closing indicator
    # right side of bool expression isn't evaluated unless left side fails
    # this may not be necessary though
    return tag[1] == '/' or tag.find('/') != -1

#debug/testing


test_text1 = "This is test text to check the [yellow]color of printed[/yellow] text. This is a second [red]color[/red] code"
test_text2 = "[yellow]This is test text to check the [green]color[/green] of printed text. This is a second [red]color[/red] code[/yellow]"

new_text1 = "This is test text to check the |yellow|color of printed|/yellow| text. This is a second |red|color|/red| code"
new_text2 = "|yellow|This is test text to check the |green|color|/green| of printed text. This is a second |red|color|/red| code|/yellow|"
gabe_text3 = "|green|Hello, world! |magenta||blue||red|Welcum to|/red| or epicc gam mad|/blue| byyyy el jacque|/magenta| and el gabo|/green|"

gabeColor(new_text2)
gabeColor(new_text1)
gabeColor(gabe_text3)


#print(color(test_text1))
#print(color(test_text2))