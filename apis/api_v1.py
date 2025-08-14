from flask import Blueprint
from flask_restx import Api


blueprint = Blueprint("v1", __name__, url_prefix="/api/v1")
api = Api(
    blueprint,
    title="Vehical Query Engine (VQE)",
    version="1.0",
    description="Welcome to the Vehical Query Engine (VQE) documentation site!"
)