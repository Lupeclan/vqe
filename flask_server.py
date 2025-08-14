from flask import Flask, Response


app = Flask(__name__)

@app.route("/ping")
def ping():
    return Response("PONG", 200, None, "text/plain")

if __name__ == "__main__":
    app.run(debug=True)
