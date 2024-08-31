#fill_char = "█"
fill_char = "|"
empty_char = " "
left_border = "["
right_border = "]"

def progressBar(progress_number, length):
    number = progress_number
    output_string = ""
    for i in range(length):
        if number > 0:
            output_string += fill_char
        else:
            output_string += empty_char
        number -= 1
    return left_border + output_string + right_border