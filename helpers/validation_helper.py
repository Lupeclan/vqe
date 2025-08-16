import flask
import functools

from typing import Optional
from json import loads


class Validate:
    def sort_field_exists(self, available_columns: list[str]):
        def decorator(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                if "sort_field" not in kwargs:
                    return func(
                        *args,
                        **kwargs,
                    )

                if (
                    kwargs["sort_field"] is not None
                    and kwargs["sort_field"] not in available_columns
                ):
                    return flask.make_response(
                        {
                            "errors": {
                                "sort_field": f"Sort field `{kwargs['sort_field']}` was not in available list of columns."
                            },
                            "message": "Input payload validation failed.",
                        },
                        400,
                    )

                return func(
                    *args,
                    **kwargs,
                )

            return inner

        return decorator


validate = Validate()
