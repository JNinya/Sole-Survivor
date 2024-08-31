import os
from sceneManager import *
#from coloredText import *

directory_of_scene_files = "scenes"


#define variable 'scenes' as a dictionary of all the scenes in specified directory
scenes = readScenes(directory_of_scene_files)
#initiate GlobalContext object using the dictionary of scenes
globalctx = GlobalContext(scenes)



#set the active scene of globalctx
globalctx.setActiveScene("start")

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


