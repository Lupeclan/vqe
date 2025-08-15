import flask
import functools

from typing import Optional
from json import loads


def parse_json_string(content: str) -> Optional[dict]:
    try:
        return loads(content)
    except (ValueError, TypeError):
        return None


class Parse:
    def query_request(self, parser):
        def decorator(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                parsed = parser.parse_args()
                parsed_query = None
                if "query" in parsed and parsed.query is not None:
                    parsed_query = parse_json_string(parsed.query)
                    if not parsed_query:
                        return flask.make_response(
                            {"error": "Invalid query supplied!"}, 400
                        )

                return func(
                    *args,
                    **kwargs,
                    sort_field=parsed.sort_field,
                    sort_order=parsed.sort_order,
                    query=parsed_query
                )

            return inner

        return decorator


parse = Parse()
