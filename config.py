import os
import json

config_help = {
    #"Example Action": "Example Action Description"
    "prefix": "Denotes the character that indicates a command."
}

default_config_filepath = os.path.join(os.path.dirname(__file__), "./default_config.json")
config_filepath = os.path.join(os.path.dirname(__file__), "./data/config.json")

# Initalizes a server's configurations. Used for the first time a bot is used in a server.
def init_config(id):
    try:
        id = str(id)

        os.makedirs(os.path.dirname(config_filepath), exist_ok=True)
        if not os.path.exists(config_filepath):
            with open(config_filepath, "w") as file:
                json.dump({}, file, indent=4)

        data = ""
        with open(config_filepath, "r") as file:
            data = json.load(file)
            if id not in data:
                with open(default_config_filepath, "r") as default_file:
                    default_config = json.load(default_file)
                    data[id] = default_config

        with open(config_filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to init config for server with id of {id} with error: {e}")

# Returns a config's value, through the given key. Returns nothing if config.json does not contain given key.
def get_config(id, key):
    try:
        id = str(id)

        with open(config_filepath, "r") as file:
            data = json.load(file)
            return data[id][key]
    except:
        return ""
    
# Sets a config option in the config.json file. Returns bool based on success, False can only be returned if given key is not already in config.
def set_config(id, key, val):
    id = str(id)

    data = ""
    with open(config_filepath, "r") as file:
        data = json.load(file)

    with open(config_filepath, "w") as file:
        if id in data and key in data[id]:
            data[id][key] = val
        else:
            return False
        
        json.dump(data, file, indent=4)
        return True
