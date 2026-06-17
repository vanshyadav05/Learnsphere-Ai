import json
import os

FILE="conversations.json"

def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE,"r") as f:
        return json.load(f)


def save(data):

    with open(FILE,"w") as f:
        json.dump(data,f)


def create_chat(name):

    data=load()

    data[name]=[]

    save(data)


def add(chat,role,msg):

    data=load()

    data[chat].append(
        {
            "role":role,
            "content":msg
        }
    )

    save(data)