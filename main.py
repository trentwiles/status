from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/')
def hello():
    FA_net = '<i class="fa-solid fa-ethernet"></i>'
    FA_server = '<i class="fa-solid fa-server"></i>'

    static = '<link rel="stylesheet" href="https://cdn-cloudfront.riverside.rocks/assets/simple.css">'
    fa_static = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'
    html = f"<!doctype html><html><head><title>Network Status</title>{static}{fa_static}</head><body><h1>Network Status</h1><br>"
    html += "<table><tr><th>Server " + FA_server + "</th><th>Traffic Levels (5 minutes)</th><th>Inbound (5 minutes)</th><th>Outbound (5 minutes)</th><th>Traffic Levels (Day)</th><th>Inbound (Day)</th><th>Outbound (Day)</th><th>All Time Bandwidth</th></tr>"
    # assuming this is going to be cached for a while
    with open('cache.json') as c:
        data = json.loads(c.read())
        for x in data:
            html += "<tr><td>" + x["server"] + "</td><td>" + x["metrics"]["current"]["average"] + "</td><td>" + x["metrics"]["current"]["inbound"] + "</td><td>" + x["metrics"]["current"]["outbound"] + "</td><td>" + x["metrics"]["daily"]["average"] + "</td><td>" + x["metrics"]["daily"]["inbound"] + "</td><td>" + x["metrics"]["daily"]["outbound"] +"</td><td>" + x["metrics"]["total"] + "</td></tr>"
    return Response(html, content_type="text/html")

if __name__ == '__main__':
    app.run()
