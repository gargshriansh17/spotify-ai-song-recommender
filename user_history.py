import json
import os

FILE="user_history.json"

def load_history():
    
    if not os.path.exists(FILE):
        return[]
    
    with open (FILE,"r") as f:
        return json.load(f)
    

def save_song(song_name):

    history=load_history()

    if song_name not in history:

        history.insert(0,song_name)

    history=history[:10]

    with open(FILE,"w") as f:
        json.dump(history,f)