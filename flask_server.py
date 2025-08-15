import logging

from os import environ
from logging.config import dictConfig

from flask import Flask, Response, redirect

from apis.api_v1 import blueprint as ns_v1
from dal.mysql import MySQLDal

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


app = Flask(__name__)
app.register_blueprint(ns_v1)

dal: MySQLDal

try:
    dal = MySQLDal()
    dal.scaffold()
except Exception:
    logging.exception("Unable to scaffold database!")
    exit(1)


@app.route("/ping")
def ping():
    return Response("PONG", 200, None, "text/plain")


@app.route("/")
def redirect_to_recommended_route():
    return redirect(environ.get("RECOMMENDED_ROUTE", "/api/v1"), 307)


if __name__ == "__main__":
    app.run(debug=True)
