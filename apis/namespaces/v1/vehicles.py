import flask

from typing import Optional
from json import loads
from flask_restx import Namespace, Resource
from http.client import responses

from apis.namespaces.v1.models.requests import get_query_parser
from apis.namespaces.v1.models.responses import get_query_result, get_validation_result
from dal.models.facts import Spaceship
from dal.mysql import MySQLDal
from helpers.parsing_helper import parse

api = Namespace("vehicles", "Vehicles", path="/vehicles")

shared_description = """
## Supported Functionality

### Operators

- AND
- OR

### Constraints

- equals
- notEquals
- startsWith
- endsWith
- contains
- notContains
- lt (Less than)
- lte (Less than or equal to)
- gt (Greater than)
- gte (Greater than or equal to)
- in
- notIn

"""
spaceship_query_description = (
    """# Examples

Query all Spaceships that have a `model` equaling `Stardust Seeker`:

```
{
    \"model\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": \"Stardust Seeker\"
            }
        ]
    }
}
```

Query all Spaceships who's models equals `Nebula Rider` or `Stardust Seeker`:

```
{
    \"model\": {
        \"operator\": \"or\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": \"Nebula Rider\"
            },
            {
                \"operator\": \"equals\",
                \"value\": \"Stardust Seeker\"
            }
        ]
    }
}
```

Query Spaceships that have a Manufacturer of `AetherForge` after year `2010`:

```
{
    \"manufacturer\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"equals\",
                \"value\": \"AetherForge\"
            }
        ]
    },
    \"year\": {
        \"operator\": \"and\",
        \"constraints\": [
            {
                \"operator\": \"gt\",
                \"value\": 2010
            }
        ]
    }
}
```

"""
    + shared_description
)


query_parser = get_query_parser(api)

spaceship_model = Spaceship.get_swagger_model(api)

dal = MySQLDal()


@api.doc(description=spaceship_query_description)
@api.route("/spaceships")
@api.response(200, responses[200], model=spaceship_model)
@api.response(500, responses[500])
class SpaceshipsResource(Resource):
    @api.expect(query_parser)
    @api.response(
        200,
        responses[200],
        model=get_query_result(api, Spaceship.__name__, spaceship_model),
    )
    @api.response(400, responses[400], model=get_validation_result(api))
    @parse.query_request(query_parser)
    def get(
        self,
        sort_field: Optional[str],
        sort_order: Optional[str],
        query: Optional[dict],
    ):
        """
        Query Spaceship Vehicles
        """

        results = dal.query(Spaceship, query, sort_field, sort_order)
        return flask.make_response({"results": results, "count": len(results)})
