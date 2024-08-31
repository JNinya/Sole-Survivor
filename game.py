from sceneManager import *

scenes = readScenes("scenes")
active_scene: Scene = scenes["start"]

print(active_scene.nextPrompt())