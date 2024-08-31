import os
from sceneManager import *


#SETUP

#from coloredText import *
directory_of_scene_files = "scenes"
#define variable 'scenes' as a dictionary of all the scenes in specified directory
scenes = readScenes(directory_of_scene_files)
#initiate GlobalContext object using the dictionary of scenes
globalctx = GlobalContext(scenes)
#set the active scene of globalctx
globalctx.setActiveScene("start")









#UTILITY FUNCTIONS

#clears the screen and prints the active scene
def printActiveScene():
    #clears the terminal
    os.system('cls')

    #selects the text for the available interactions
    interactions_list = list(globalctx.active_scene.nextInteractions().keys())

    #print prompt
    print(globalctx.active_scene.nextPrompt()["text"])

    print("")

    #print interactions
    for i in range(len(interactions_list)):
        print(f"{i+1}: {interactions_list[i]}")


#activates interactions in current scene based on number input
def interact(interaction_number):

    interaction_number = int(interaction_number)

    #gets interactions that fit requirements
    interactions_list = list(globalctx.active_scene.nextInteractions().values())

    updateStates(interactions_list[interaction_number-1], globalctx)






#GAMELOOP

while True:
    #clears the screen and prints the active scene
    printActiveScene()

    interact(input())




#IDEAS

"""
Add support for if the player inputs something other than a number or an out of range number
impletment changing of states with global.active_state
add support for math operators in interaction requirements
"""