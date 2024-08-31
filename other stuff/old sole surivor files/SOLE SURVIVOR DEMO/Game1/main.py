import os
import fh
import parseScene

# Main game loop
def gameloop(scene):
    # Clear the screen
    os.system('cls')

    # Parsing & printing the text (done with the parseScenes module)
    print(parseScene.description(scene))

    # Interpret user input. Selects destination scene
    choice = input().upper()
    scene = str(scene)
    pointerMap = parseScene.where(scene)
    if choice in pointerMap:
        destinationScene = parseScene.where(scene)[choice]
    else:
        gameloop(scene)

    # Open new scene that the user chose
    gameloop(destinationScene)

# Start the game
os.system('color a')
gameloop(0)

# end by gabe