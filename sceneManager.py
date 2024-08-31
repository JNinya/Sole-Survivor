"""
Functions:

readscene(scenes_dir, scene_name)
readscenes(scenes_dir)

"""

import os
import json
import fh

# TODO: determine whether this is necessary/wanted
class Prompt:
    def __init__(self, prompts_dict):
        self.text = prompts_dict["text"]
        self.requirements = prompts_dict["requirements"]

    def __str__(self):
        return f"Text: {self.text}\nRequirements: {self.requirements}"

class Scene:
    def __init__(self, name, json_dict, globalctx: GlobalContext = None):
        self.globalctx: GlobalContext = globalctx

        self.name: str = name.replace(".json", "")
        self.states = json_dict["states"]
        self.interactions = json_dict["interactions"]
        
        self.prompts = json_dict["prompts"]
        #for json_prompt in json_dict["prompts"]:
        #    self.prompts.append(Prompt(json_prompt))

        self.adjacent_scenes = json_dict["adjacent_scenes"]
    
    def __str__(self):
        return f"States:\n{self.states}\n\nInteractions:\n{self.interactions}\n\nPrompts:\n{self.prompts}\n\nAdjacent scenes:\n{self.adjacent_scenes}"
    
    # Selects the next prompt based on current states
    # Returns a string containing the text to display
    def nextPrompt(self):
        # For each requirement, check if current states match prompt required states
        for prompt in self.prompts:
            if promptFitsState(prompt, self, self.globalctx.scenes):
                return prompt
        # TODO: raise custom NoPromptFoundError
        print(f"WARNING: no prompt was found to fit required state for scene {self.name}")
        return None

    # Returns an array of interactions available based on current states
    def nextInteractions(self):
        interactions = {}
        for interaction in self.interactions:
            interact_data = self.interactions[interaction]
            if interactionFitsState(interact_data, self):
                interactions[interaction] = interact_data
        return interactions
    
# end def Scene

class GlobalContext:
    # scenes are either loaded or a directory name
    def __init__(self, scenes: dict[str, Scene] | str):
        if isinstance(scenes, dict[str, Scene]):
            for scene in scenes.values():
                scene.globalctx = self
            self.scenes = scenes
        elif isinstance(scenes, str):
            self.scenes = readScenes(scenes)

        self.active_scene: Scene = None

    def setActiveScene(self, scene: Scene | str):
        actual_scene = None
        if isinstance(scene, Scene):
            actual_scene = scene
        elif isinstance(scene, str):
            actual_scene = self.scenes[scene]
        
        if actual_scene is None:
            raise ValueError("Warning") # TODO: change to warning for setting void scene
        self.active_scene = actual_scene


# Returns boolean indicating whether the prompt meets state requirements
def promptFitsState(prompt, scene, scenes):
    for req_state in prompt["requirements"]:
        state_val = readState(req_state, scene, scenes)
        #print(req_state, prompt["requirements"][req_state], state_val) # DEBUG
        if prompt["requirements"][req_state] != state_val:
            return False
    return True

# Returns boolean indicating whether the interaction meets state requirements
def interactionFitsState(interact_data, scene, scenes):
    for req_state in interact_data["requirements"]:
        state_val = readState(req_state, scene, scenes)
        if interact_data["requirements"][req_state] != state_val:
            return False
    return True

# Read scene file as scene object
def readScene(scenes_dir, scene_name):
    raw_text = fh.read(f"{scenes_dir}/{scene_name}")
    json_dict = json.loads(raw_text)
    scene = Scene(scene_name, json_dict)

    return scene


# Read all scenes in a directory into a map of string keys (scene names) and scene values (scene data)
def readScenes(scenes_dir):
    scene_map = {}
    for file in os.listdir(scenes_dir):
        if file.endswith(".json"):
            scene_map[file.replace(".json", "")] = readScene(scenes_dir, file)

    return scene_map

# Update game state based on interaction selected
def updateStates(interaction, scene, scenes_dict):
    for update in interaction["updates"]:
        setState(update, interaction["updates"][update], scene, scenes_dict)

# Get state value from local, scene, or global path
# Examples: "global.scene", "lab_scene_3.LIGHTS_ON", "LIGHTS_ON"
# state_path is the string path to get the state
# scene is the current active scene
# scenes_dict is all the scenes to be accessed
def readState(state_path: str, scene: Scene, scenes_dict: list[Scene]):
    split_path = state_path.split(".")
    if len(split_path) > 1:
        if split_path[0] == "global":
            # query global state
            raise NotImplementedError("Need to query global state!")
        else:
            # query scene state
            return scenes_dict[split_path[0]].states[split_path[1]]

    else:
        # local path
        return scene.states[state_path]

def setState(state_path, value, scene, scenes_dict):
    split_path = state_path.split(".")
    if len(split_path) > 1:
        if split_path[0] == "global":
            # set global state
            raise NotImplementedError("Need to set global state!")
        else:
            # set scene state
            scenes_dict[split_path[0]].states[split_path[1]] = value

    else:
        # local path
        scene.states[state_path] = value


"""
# Debug/Testing

# Load scenes from directory
#scenes = readScenes("scenes")
#scene: Scene = scenes["start"]

#print(readState("LIGHTS_ON", scene, scenes))
#prompt = scene.nextPrompt()

# Print prompt and interactions based on initial state
# For lab_scene_3, I set the lights to initially be on 
print(scene.nextPrompt()["text"])
interactions = scene.nextInteractions()
print(interactions)

# This is magic right here. The first interaction is the light switch interaction,
# so let's update the state based on that interaction
updateStates(interactions["Turn on the light"], scene, scenes)

# Let's print the new state results and see!
print("\n")
print(scene.nextPrompt()["text"])
print(scene.nextInteractions())
"""