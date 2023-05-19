import requests
import json

def fetch():
    with open("servers.json", 'r') as s:
        x = json.load(s)
        for z in x:
            api = requests.get(z["endpoint"] + "/data", headers={"User-agent": "trent"})

fetch()