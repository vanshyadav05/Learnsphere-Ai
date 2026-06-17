import json
import os

FILE="memory.json"


def load():

    if not os.path.exists(FILE):

        return {}

    with open(FILE,"r") as f:

        return json.load(f)


def save(data):

    with open(FILE,"w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


def add(chat,role,text):

    data=load()

    if chat not in data:

        data[chat]=[]

    data[chat].append({

        "role":role,
        "content":text

    })

    save(data)


def get(chat):

    data=load()

    return data.get(chat,[])


def remove(chat):

    data=load()

    if chat in data:

        del data[chat]

    save(data)