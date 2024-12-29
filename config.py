import os
import json

config_help = {
    #"Example Action": "Example Action Description"
    "prefix": "Denotes the character that indicates a command."
}

config_filepath = os.path.join(os.path.dirname(__file__), "./config.json")

# Returns a config's value, through the given key. Returns nothing if config.json does not contain given key.
def get_config(key):
    try:
        with open(config_filepath, "r") as file:
            return json.load(file)[key]
    except:
        return ""
    
# Sets a config option in the config.json file. Returns bool based on success, False can only be returned if given key is not already in config.
def set_config(key, val):
    data = ""
    with open(config_filepath, "r") as file:
        data = json.load(file)

    with open(config_filepath, "w") as file:
        if key in data:
            data[key] = val
        else:
            return False
        
        json.dump(data, file, indent=4)
        return True
