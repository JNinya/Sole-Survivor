"""
Functions:

description(sceneId)

where(sceneId)

"""

import fh

# Get description text from the selected scene file
def description(sceneId):
    # rawText gets the whole file in the raw
    rawText = fh.read("scenes/" + str(sceneId))

    # split based on the ';' operator
    splitText = rawText.split(";\n")
    
    # return just the description (before the ; operator)
    return splitText[0]

# Read map of options to scene ids from scene file
# sceneId -> id/name of scene file
# Returns a map of pointers with string indices (option ids) and int values (scene ids)
def where(sceneId):
    # rawText gets the whole file in the raw
    rawText = fh.read("scenes/" + str(sceneId))

    # split based on the ';' operator
    splitText = rawText.split(";\n")

    # read pointers into map
    pointers = splitText[1].splitlines()
    pointer_map = {}
    for pointer in pointers:
        pointer = pointer.split(">")
        pointer_map[pointer[0]] = int(pointer[1])

    return pointer_map
