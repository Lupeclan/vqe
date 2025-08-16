from flask_restx import fields


def get_query_result(api, result_object_name: str, result_model):
    return api.model(
        f"{result_object_name}QueryResult",
        {
            "results": fields.List(
                fields.Nested(api.model(result_object_name, result_model)),
                description=f"List of {result_object_name} objects",
            ),
            "count": fields.Integer(
                1, description=f"Number of {result_object_name} in the results list"
            ),
        },
    )


def get_validation_result(api):
    return api.model(
        "ValidationResult",
        {
            "errors": fields.Wildcard(
                fields.String(),
                description="Dictionary of the parameter name and it's validation error.",
            ),
            "message": fields.String(
                "Input payload validation failed",
                description="Description of the error in the payload.",
            ),
        },
    )


def get_unhandled_error(api):
    return api.model(
        "ErrorResult",
        {
            "message": fields.String(
                "Internal Server Error!",
                description="Details about the server error.",
            )
        },
    )
