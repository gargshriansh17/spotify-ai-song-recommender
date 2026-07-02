import json
import os

LIKED_FILE="liked_songs.json"
DISLIKED_FILE="disliked_songs.json"

def load_liked():
    if not os.path.exists(LIKED_FILE):
        return []
    
    with open(LIKED_FILE,"r") as f:
        return json.load(f)
    

def save_liked(song):
    songs=load_liked()

    if song not in songs:
        songs.append(song)

    with open(LIKED_FILE,"w") as f:
        json.dump(songs,f)


def load_disliked():
    if not os.path.exists(DISLIKED_FILE):
        return []
    
    with open(DISLIKED_FILE,"r") as f:
        return json.load(f)
    

def save_disliked(song):
    songs=load_disliked()

    if song not in songs:
        songs.append(song)

    with open(DISLIKED_FILE,"w") as f:
        json.dump(songs,f)