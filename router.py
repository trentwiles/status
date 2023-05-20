from flask import Flask, Response
import json
import subprocess
import datetime

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
    current_time = datetime.datetime.utcnow()
    start_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 0, 0, 0)
    time_difference = current_time - start_time
    seconds_since_midnight = time_difference.total_seconds()

    Daverage = ((DcurrentIn + DcurrentOut) / (seconds_since_midnight) ) * 8.3
    if DcurrentOut > 1000 or DcurrentIn > 1000:
        DcurrentOut /= 1024
        DcurrentIn /= 1024
        Dmeasure = "GB"

    print(json.dumps(today))
    allTime  = (vnstat["interfaces"][0]["traffic"]["total"]["rx"] + vnstat["interfaces"][0]["traffic"]["total"]["rx"])
    return Response(json.dumps({"current": {"inbound": str(round(currentIn, 2)) + measure, "outbound": str(round(currentOut, 2)) + measure, "average": str(round(average, 2)) + bw}, "daily": {"inbound": str(round(DcurrentIn, 2)) + Dmeasure, "outbound": str(round(DcurrentOut, 2)) + Dmeasure, "average": str(round(Daverage, 2)) + Dbw}, "total": str(round(allTime/ 1024 ** 4, 2)) + "TB"}), content_type="application/json")

if __name__ == '__main__':
    app.run(port=8585, host='0.0.0.0')
