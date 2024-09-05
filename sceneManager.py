import os
import json
from typing import cast
import fh



class GlobalContext():
    pass


type JSONDict = dict[str, object]

class Interaction:
    def __init__(self, name: str, data: JSONDict):
        self.name: str = name
        self.requirements: JSONDict = data["requirements"]
        self.updates: JSONDict = data["updates"]

    def __str__(self):
        return f"Name: {self.name}\nRequirements: {self.requirements}\nUpdates: {self.updates}"

class Prompt:
    def __init__(self, prompts_dict: JSONDict):
        self.text: str = prompts_dict["text"]
        self.requirements: JSONDict = prompts_dict["requirements"]

    def __str__(self):
        return f"Text: {self.text}\nRequirements: {self.requirements}"

class Scene:
    def __init__(self, name: str, json_dict: JSONDict, globalctx: GlobalContext = None):
        self.globalctx: GlobalContext = globalctx

        self.name: str = name.replace(".json", "")
        self.states = json_dict["states"]
        
        self.interactions: dict[str, Interaction] = {}
        for name, data in json_dict["interactions"].items():
            self.interactions[name] = Interaction(name, data)
        
        self.prompts: list[Prompt] = []
        for json_prompt in json_dict["prompts"]:
            self.prompts.append(Prompt(json_prompt))

        self.adjacent_scenes = json_dict.get("adjacent_scenes", None)
    
    def __str__(self):
        return f"States:\n{self.states}\n\nInteractions:\n{self.interactions}\n\nPrompts:\n{self.prompts}\n\nAdjacent scenes:\n{self.adjacent_scenes}"
    
    # Selects the next prompt based on current states
    # Returns a string containing the text to display
    def nextPrompt(self):
        # For each requirement, check if current states match prompt required states
        for prompt in self.prompts:
            if promptFitsState(prompt, self, self.globalctx):
                return prompt
        # TODO: raise custom NoPromptFoundError
        print(f"WARNING: no prompt was found to fit required state for scene {self.name}")
        return None

    # Returns an array of interactions available based on current states
    def nextInteractions(self) -> dict[str, Interaction]:
        interactions: dict[str, Interaction] = {}
        for name, interact_data in self.interactions.items():
            if interactionFitsState(interact_data, self, self.globalctx):
                interactions[name] = interact_data
        return interactions
    
# end def Scene

class GlobalStateException(Exception):
    pass

class GlobalContext:
    # scenes are either loaded or a directory name
    def __init__(self, scenes_or_dir: dict[str, Scene] | str, global_filename: str | None, starting_scene: str | None = None):
        self.scenes: dict[str, Scene] = None
        if isinstance(scenes_or_dir, dict):
            for scene in scenes_or_dir.values():
                scene.globalctx = self
            self.scenes = scenes_or_dir
        elif isinstance(scenes_or_dir, str):
            self.scenes = readScenes(scenes_or_dir, self)

        global_filedata: JSONDict = None
        if global_filename is not None:
            # TODO: better error handling here
            content = fh.read(f"{global_filename}.json")
            global_filedata = json.loads(content)

        self.states: JSONDict = global_filedata["states"] if global_filedata is not None else {}

        self.active_scene: Scene = None
        if starting_scene is not None:
            self.setActiveScene(starting_scene)
        

    def setActiveScene(self, scene: Scene | str):
        actual_scene = None
        if isinstance(scene, Scene):
            actual_scene = scene
        elif isinstance(scene, str):
            actual_scene = self.scenes[scene]
        
        if actual_scene is None:
            raise GlobalStateException("Requested scene to be active is None")
        self.active_scene = actual_scene

    # TODO: return old value after setting new?
    def setGlobalState(self, state_path: str, value: object):
        match state_path:
            case "active_scene":
                self.setActiveScene(cast(str, value))

            case _:
                self.states[state_path] = value
                #raise GlobalStateException(f"Unknown global state path to set ({state_path})")
            
    def readGlobalState(self, state_path: str) -> object:
        match state_path:
            case "active_scene":
                return self.active_scene.name

            case _:
                return self.states[state_path]
                #raise GlobalStateException(f"Unknown global state path to read ({state_path})")

# Returns boolean indicating whether the prompt meets state requirements
def promptFitsState(prompt: Prompt, scene: Scene, globalctx: GlobalContext):
    for req_state_path in prompt.requirements.keys():
        state_val = readState(req_state_path, globalctx, scene)
        if prompt.requirements[req_state_path] != state_val:
            return False
    return True

# Returns boolean indicating whether the interaction meets state requirements
def interactionFitsState(interact: Interaction, scene: Scene, globalctx: GlobalContext):
    for req_state_path in interact.requirements.keys():
        state_val = readState(req_state_path, globalctx, scene)
        if interact.requirements[req_state_path] != state_val:
            return False
    return True

# Read scene file as scene object
def readScene(scenes_dir: str, scene_name: str, globalctx: GlobalContext = None):
    raw_text = fh.read(f"{scenes_dir}/{scene_name}")
    json_dict = json.loads(raw_text)
    scene = Scene(scene_name, json_dict, globalctx)

    return scene


# Read all scenes in a directory into a map of string keys (scene names) and scene values (scene data)
def readScenes(scenes_dir, globalctx: GlobalContext = None):
    scene_map = {}
    for file in os.listdir(scenes_dir):
        if file.endswith(".json"):
            scene_map[file.replace(".json", "")] = readScene(scenes_dir, file, globalctx)

    return scene_map

# Update game state based on interaction selected
def updateStates(interaction: Interaction, globalctx: GlobalContext):
    for state_path, update_val in interaction.updates.items():
        setState(state_path, update_val, globalctx)

# Get state value from local, scene, or global path
# Examples: "global.scene", "lab_scene_3.LIGHTS_ON", "LIGHTS_ON"
# state_path is the string path to get the state
# scene is the current active scene
# scenes_dict is all the scenes to be accessed
def readState(state_path: str, globalctx: GlobalContext, active_scene: Scene = None):
    active_scene = active_scene if active_scene is not None else globalctx.active_scene

    split_path = state_path.split(".")
    if len(split_path) > 1:
        if split_path[0] == "global":
            # query global state
            return globalctx.readGlobalState(split_path[1])
        else:
            # query scene state
            return globalctx.scenes[split_path[0]].states[split_path[1]]

    else:
        # local path
        return active_scene.states[state_path]

def setState(state_path: str, value: object, globalctx: GlobalContext, active_scene: Scene = None):
    active_scene = active_scene if active_scene is not None else globalctx.active_scene
    
    split_path = state_path.split(".")
    if len(split_path) > 1:
        if split_path[0] == "global":
            # set global state
            globalctx.setGlobalState(split_path[1], value)
        else:
            # set scene state
            globalctx.scenes[split_path[0]].states[split_path[1]] = value

    else:
        # local path
        active_scene.states[state_path] = value

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