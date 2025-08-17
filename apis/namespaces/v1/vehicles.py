import flask

from typing import Optional
from json import loads
from flask_restx import Namespace, Resource
from http.client import responses

from sample_data.payloads import (
    bike_gears_and_type_and_year,
    car_colours,
    car_make_and_year,
    car_less_than_or_equal_seats,
    spaceship_singular_model,
    spaceship_two_models,
    spaceship_manufacturer_and_year
)

from apis.namespaces.v1.models.requests import get_query_parser
from apis.namespaces.v1.models.responses import (
    get_query_result,
    get_validation_result,
    get_unhandled_error,
)
from dal.models.dimensions import Manufacturer, Model
from dal.models.facts import Spaceship, Car, Bike
from dal.mysql import MySQLDal
from helpers.parsing_helper import parse
from helpers.validation_helper import validate

api = Namespace("vehicles", "Vehicles", path="/vehicles")

query_parser = get_query_parser(api)
error_model = get_unhandled_error(api)

dal = MySQLDal()

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

```"""
 + spaceship_singular_model + 
"""```

Query all Spaceships who's `model` equals `Nebula Rider` or `Stardust Seeker`:

```"""
 + spaceship_two_models + 
"""```

Query Spaceships that have a `manufacturer` of `AetherForge` after year `2010`:

```"""
 + spaceship_manufacturer_and_year + 
"""```

"""
    + shared_description
)


def build_response(results: Optional[list[dict]]):
    if results:
        return flask.make_response({"results": results, "count": len(results)})

    return flask.make_response({"results": [], "count": 0})


spaceship_model = Spaceship.get_swagger_model(api)


@api.doc(description=spaceship_query_description)
@api.route("/spaceships")
@api.response(200, responses[200], model=spaceship_model)
@api.response(500, responses[500], model=error_model)
class SpaceshipsResource(Resource):
    @api.expect(query_parser)
    @api.response(
        200,
        responses[200],
        model=get_query_result(api, Spaceship.__name__, spaceship_model),
    )
    @api.response(400, responses[400], model=get_validation_result(api))
    @parse.query_request(query_parser)
    @validate.sort_field_exists(
        Spaceship.query_columns + Manufacturer.query_columns + Model.query_columns
    )
    def get(
        self,
        sort_field: Optional[str],
        sort_order: Optional[str],
        query: Optional[dict],
    ):
        """
        Query Spaceship Vehicles
        """
        return build_response(dal.query(Spaceship, query, sort_field, sort_order))


car_query_description = (
    """# Examples

Query all Cars that have a `seats` less than or equal to `7`:

```"""
 + car_less_than_or_equal_seats + 
"""```

Query all Cars who's `colour` starts with `Light` and contains `Y`:

```"""
 + car_colours + 
"""```

Query Cars that have a year in `1971,2002` and a `make` that ends with `s`:

```"""
 + car_make_and_year + 
"""```

"""
    + shared_description
)

car_model = Car.get_swagger_model(api)


@api.doc(description=car_query_description)
@api.route("/cars")
@api.response(200, responses[200], model=car_model)
@api.response(500, responses[500], model=error_model)
class CarsResource(Resource):
    @api.expect(query_parser)
    @api.response(
        200,
        responses[200],
        model=get_query_result(api, Car.__name__, car_model),
    )
    @api.response(400, responses[400], model=get_validation_result(api))
    @parse.query_request(query_parser)
    @validate.sort_field_exists(
        Car.query_columns + Manufacturer.query_columns + Model.query_columns
    )
    def get(
        self,
        sort_field: Optional[str],
        sort_order: Optional[str],
        query: Optional[dict],
    ):
        """
        Query Car Vehicles
        """
        return build_response(dal.query(Car, query, sort_field, sort_order))


bike_query_description = (
    """# Examples

Query Bikes that have a `gears` greater than `3`, a `type` that is not `BMX` or `Road`:

```"""
 + bike_gears_and_type_and_year + 
"""```

"""
    + shared_description
)

bike_model = Bike.get_swagger_model(api)


@api.doc(description=bike_query_description)
@api.route("/bikes")
@api.response(200, responses[200], model=bike_model)
@api.response(500, responses[500], model=error_model)
class BikesResource(Resource):
    @api.expect(query_parser)
    @api.response(
        200,
        responses[200],
        model=get_query_result(api, Bike.__name__, bike_model),
    )
    @api.response(400, responses[400], model=get_validation_result(api))
    @parse.query_request(query_parser)
    @validate.sort_field_exists(
        Bike.query_columns + Manufacturer.query_columns + Model.query_columns
    )
    def get(
        self,
        sort_field: Optional[str],
        sort_order: Optional[str],
        query: Optional[dict],
    ):
        """
        Query Bike Vehicles
        """
        return build_response(dal.query(Bike, query, sort_field, sort_order))
