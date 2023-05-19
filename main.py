from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def hello():
    return Response("Hey!", content_type="application/json")

if __name__ == '__main__':
    app.run()
