from flask import Flask, Response
import json
import subprocess

app = Flask(__name__)


@app.route('/')
def hello():
    command = ['vnstat', '--json']
    vnstat = json.loads(subprocess.check_output(command).decode('utf-8'))
    """
    LAST FIVE MINUTES
    """
    currentData = vnstat["interfaces"][0]["traffic"]["fiveminute"][len(vnstat["interfaces"][0]["traffic"]["fiveminute"]) - 1]
    currentIn = round(currentData["rx"] / 1024 ** 2, 2)

    currentOut = round(currentData["tx"] / 1024 ** 2, 2)

    measure = "MB"
    bw = "mbps"
    average = ((currentIn + currentOut) / (5 * 60) ) * 8.3
    if currentOut > 1000 or currentIn > 1000:
        currentOut /= 1024
        currentIn /= 1024
        measure = "GB"
        bw = "gbps"
        average /= 1000
    
    """
    Daily
    """
    today = vnstat["interfaces"][0]["traffic"]["day"][len(vnstat["interfaces"][0]["traffic"]["day"]) - 1]
    DcurrentIn = round(today["rx"] / 1024 ** 2, 2)

    DcurrentOut = round(today["tx"] / 1024 ** 2, 2)

    Dmeasure = "MB"
    Dbw = "mbps"
    Daverage = ((DcurrentIn + DcurrentOut) / (24 * 3660) ) * 8.3
    if DcurrentOut > 1000 or DcurrentIn > 1000:
        DcurrentOut /= 1024
        DcurrentIn /= 1024
        Dmeasure = "GB"

    print(json.dumps(today))
    allTime  = (vnstat["interfaces"][0]["traffic"]["total"]["rx"] + vnstat["interfaces"][0]["traffic"]["total"]["rx"])
    return Response(json.dumps({"current": {"inbound": str(currentIn) + measure, "outbound": str(currentOut) + measure, "average": str(round(average, 2)) + bw}, "daily": {"inbound": str(round(DcurrentIn, 2)) + Dmeasure, "outbound": str(round(DcurrentOut, 2)) + Dmeasure, "average": str(round(Daverage, 2)) + Dbw}, "total": str(round(allTime/ 1024 ** 4, 2)) + "TB"}), content_type="application/json")

if __name__ == '__main__':
    app.run(port=6565)
