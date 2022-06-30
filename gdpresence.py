import sys
import threading
import requests
import gd
import time
from pypresence import Presence
import os.path
import json

##def not stolen from C#
def isnoneorempty(string):
    if string == None:
        return True
    string2 = string.replace(" ", "")
    if len(string2) == 0:
        return True
    else:
        if not string2:
            return True
        else:
            return False

def gdpexit():
    sys.exit(0)


##Playing {Map_Name} {Percent}
##Attempt {Attempt #} Difficulty: {Difficulty}
def getgdinfo():
    attempt = gdmemory.get_attempt()
    mapname = gdmemory.get_level_name()
    difficulty = str(gdmemory.get_level_difficulty())
    percent = int(gdmemory.get_percent())
    scene = str(gdmemory.get_scene())
    difficultynum = int(gdmemory.get_level_difficulty_value())
    practice = gdmemory.is_practice_mode()
    leveltype = gdmemory.get_level_type()
    id = gdmemory.get_level_id_fast()
    gdinfo = {
        "attempt": attempt,
        "mapname": mapname,
        "difficulty": difficulty.replace("LevelDifficulty.", "").replace("DemonDifficulty.", "").replace("_", " "),
        "percent": percent,
        "scene": scene.replace("Scene.", ""),
        "difficultynum": difficultynum,
        "practice": practice,
        "leveltype": leveltype,
        "id": id
    }
    return gdinfo


def update():
    info = getgdinfo()
    attempt = info["attempt"]
    mapname = info["mapname"]
    difficulty = info["difficulty"].title()
    percent = info["percent"]
    scene = info["scene"]
    difficultynum = info["difficultynum"]
    practice = info["practice"]
    leveltype = info["leveltype"]
    id = info["id"]
    if attempt == 0 or mapname == "":
        localconfig["state"] = "Menu or Editor"
        localconfig["details"] = None
    else:
        if difficulty == "Na":
            if difficultynum == 0:
                i = 0
                for x in officiallevellist.get("levels"):
                    if x.get("name") == mapname:
                        found = True
                        break
                    else:
                        found = False
                        i += 1
                if found == True:
                    difficulty = officiallevellist.get("levels")[i].get("difficulty").title()
                else:
                    difficulty = "NA"
        if practice == True:
            mode = "Practice"
        else:
            mode = "Normal"
        localconfig["state"] = f"Playing {mapname} {mode} Mode {percent}%"
        localconfig["details"] = f"Attempt {attempt} Difficulty {difficulty}"
    client.update(state=localconfig["state"], details=localconfig["details"], large_image=localconfig["large_img"],
                      small_image=localconfig["small_img"],
                      large_text=localconfig["large_txt"], start=localconfig["start"])
    return

def start():
    print("Connecting...")
    client.connect()
    print("Connected!")
    print("You can kill the script with Control-C!")
    try:
        while True:
            update()
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Exiting...")
        print("Closing connection...")
        client.close()
        gdpexit()

def saveconfig():
    print("Saving config...")
    with open("config.json", "w") as sconf:
        json.dump(config, sconf, ensure_ascii=False)
    print("Config saved!")
    return

def getconfig():
    print("Loading config file...")
    if os.path.isfile("config.json") == False:
        print("No config file found!")
        print("Creating new one...")
        newconfig = {
            "client_id": ""
        }
        with open("config.json", "w") as saveconfig:
            json.dump(newconfig, saveconfig, ensure_ascii=False)
        print("Created new config!")
        return newconfig
    with open("config.json", "r") as loadconfig:
        lconf = json.load(loadconfig)
        return lconf

try:
    gdmemory = gd.memory.get_memory()
except RuntimeError:
    print("You need to start gd before starting this script! Exiting...")
    gdpexit()

print("Getting client id...")
config = getconfig()
if isnoneorempty(config.get("client_id")) == True:
    print("Enter your client id:")
    new_client_id = input("#")
    if isnoneorempty(new_client_id) == True:
        print("Nothing is entered! Exiting...")
        gdpexit()
    config["client_id"] = new_client_id
    saveconfig()

print("Getting discord client...")
client = Presence(config.get("client_id"))

print("Setting local variables...")
localconfig = {
    "state": "placeholder",
    "details": "placeholder",
    "large_img": "https://upload.wikimedia.org/wikipedia/en/thumb/3/35/Geometry_Dash_Logo.PNG/250px-Geometry_Dash_Logo.PNG",
    "small_img": "placeholder",
    "large_txt": "Geometry Dash",
    "start": time.time()
}

def debugmenu():
    debugchoice = input(">")
    if debugchoice == "help":
        print("-help (shows this screen)")
        print("-exit (exists the program)")
        print("-changestate (changes state)")
        print("-changedetails (changes details)")
        print("-changelargeimg (changes large image)")
        print("-changesmallimg (changes small image)")
        print("-changelargetxt (changes large image)")
        print("-resettimer (resets the timer)")
        print("-getconfig (prints config to the screen)")
        debugmenu()
    elif debugchoice == "exit":
        print("Stopped debug! Kill loop with Control-C!")
        gdpexit()
    elif debugchoice == "changestate":
        print("New state:")
        nstate = input("?")
        localconfig["state"] = nstate
        print("Changed state to " + nstate + "!")
        debugmenu()
    elif debugchoice == "changedetails":
        print("New details:")
        ndetails = input("?")
        localconfig["details"] = ndetails
        print("Changed details to " + ndetails + "!")
        debugmenu()
    elif debugchoice == "changelargeimg":
        print("New large image:")
        nlargeimg = input("?")
        localconfig["large_img"] = nlargeimg
        print("Changed large image to " + nlargeimg + "!")
        debugmenu()
    elif debugchoice == "changesmallimg":
        print("New small image:")
        nsmallimg = input("?")
        localconfig["small_img"] = nsmallimg
        print("Changed small image to " + nsmallimg + "!")
        debugmenu()
    elif debugchoice == "changelargetxt":
        print("New large text:")
        nlargetext = input("?")
        localconfig["large_txt"] = nlargetext
        print("Changed large text to " + nlargetext + "!")
        debugmenu()
    elif debugchoice == "resettimer":
        localconfig["start"] = time.time()
        print("Timer reset!")
        debugmenu()
    elif debugchoice == "getconfig":
        print(localconfig)
        debugmenu()
    else:
        debugmenu()

if config.get("debug", None) != None:
    if config.get("debug") == True:
        print("Enabled debug mode!")
        threading.Thread(target=debugmenu).start()

##because apparently offcical level ids doesnt exist >:(
print("Getting list...")
officiallevellist = requests.get("https://martin0300.github.io/backend/pydiscordrpc.json").json()

print("Starting...")
start()


