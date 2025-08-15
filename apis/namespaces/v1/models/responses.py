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
            "error": fields.String(
                "Invalid query supplied!",
                description="Description of the error in the payload.",
            )
        },
    )
