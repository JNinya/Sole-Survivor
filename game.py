import os
from typing import Final
from sceneManager import *


#SETUP

#from coloredText import *

SCENE_DIR: Final[str] = "scenes"

#scenes = readScenes(SCENE_DIR)

globalctx = GlobalContext(SCENE_DIR)
globalctx.setActiveScene("start")









#UTILITY FUNCTIONS

#clears the screen and prints the active scene
def printActiveScene():
    #clears the terminal
    os.system('cls')

    #selects the text for the available interactions
    interactions_list = list(globalctx.active_scene.nextInteractions().keys())

    #print prompt
    print(globalctx.active_scene.nextPrompt().text)

    print("")

    #print interactions
    for i in range(len(interactions_list)):
        print(f"{i+1}: {interactions_list[i]}")


#activates interactions in current scene based on number input
def interact(interaction_number):
    
    # the try/except/else block will handle any bad inputs because it will only run if a valid number choice is entered,
    # otherwise it will just refresh the screen. If an error arises at another point 
    # it will still allow that error through for debugging purposes
    try:
        interaction_number = int(interaction_number)

        #gets interactions that fit requirements
        interactions_list = list(globalctx.active_scene.nextInteractions().values())

    except:
        return None
    
    else:
        if ((interaction_number > 0) and (interaction_number <= len(interactions_list))):
            updateStates(interactions_list[interaction_number-1], globalctx)
        else:
            return None







#GAMELOOP

while True:
    #clears the screen and prints the active scene
    printActiveScene()

    interact(input())




#IDEAS

"""
DONE BY JACK!!!!!!!!!!!!! Add support for if the player inputs something other than a number or an out of range number
impletment changing of states with global.active_scene
add support for math operators in interaction requirements
"""