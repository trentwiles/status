import requests
import json
import os

def fetch():
    with open("servers.json", 'r') as s:
        load = []
        x = json.load(s)
        for z in x:
            api = requests.get("http://" + z["endpoint"] + ":8585/", headers={"User-agent": "trent"})
            x = {"server": (z["desc"] + " (" + z["IATA"] + ")"), "metrics": api.json()}
            load.append(x)
    #os.remove("cache.json")
    with open("cache.json", 'a') as w:
        w.write(json.dumps(load))
        w.close()

fetch()