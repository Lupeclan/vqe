from os import environ

from flask import Flask, Response, redirect

from apis.api_v1 import blueprint as ns_v1

app = Flask(__name__)

app.register_blueprint(ns_v1)


@app.route("/ping")
def ping():
    return Response("PONG", 200, None, "text/plain")


@app.route("/")
def redirect_to_recommended_route():
    return redirect(environ.get("RECOMMENDED_ROUTE", "/api/v1"), 307)


if __name__ == "__main__":
    app.run(debug=True)
