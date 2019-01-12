from ezy_multiplayer import *
import pickle, os

def load_settings():
    try:
        if os.name == "nt":
            return pickle.load(open("settings.data", "rb"))
        else:
            return pickle.load(open("root/settings.data", "rb"))
    except Exception as e:
        print(e)
        return "False"
        
def save_settings(everything):
    try:
        if os.name == "nt":
            pickle.dump(everything, open("settings.data", "wb"))
        else: 
            pickle.dump(everything, open("root/settings.data", "wb"))
        return "True"
    except Exception as e:
        print(e)
        return "False"

def send_back(data):
    if data == "get_everything":
        return load_settings()
    elif type(data) == dict:
        return save_settings(data["set_everything"])
    return data
    
port = get_free_port()

print("Local Hostname: " + get_ip())
print("Port: %s" % str(port))

newLobby(port, send_back)
while True:pass