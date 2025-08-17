import unittest

from ddt import ddt, data
from flask_server import app


@ddt
class VehiclesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

        return super().setUp()

    @data(
        "/api/v1/vehicles/spaceships",
        "/api/v1/vehicles/cars",
        "/api/v1/vehicles/bikes",
    )
    def test_invalid_query_json(self, path: str) -> None:
        response = self.client.get(
            path,
            query_string='query={"model":{"operator":"and"}',
        )

        self.assertEqual("400 BAD REQUEST", response.status)
        self.assertEqual(
            b'{"errors":{"query":"Invalid query supplied, see Examples for query payload."},"message":"Input payload validation failed."}\n',
            response.data,
        )
        self.assertEqual("application/json", response.mimetype)

    @data(
        "/api/v1/vehicles/spaceships",
        "/api/v1/vehicles/cars",
        "/api/v1/vehicles/bikes",
    )
    def test_not_present_sort_field(self, path: str) -> None:
        response = self.client.get(
            path,
            query_string="sort_field=generation",
        )

        self.assertEqual("400 BAD REQUEST", response.status)
        self.assertEqual(
            b'{"errors":{"sort_field":"Sort field `generation` was not in available list of columns."},"message":"Input payload validation failed."}\n',
            response.data,
        )
        self.assertEqual("application/json", response.mimetype)

    @data(
        "/api/v1/vehicles/spaceships",
        "/api/v1/vehicles/cars",
        "/api/v1/vehicles/bikes",
    )
    def test_all_results(self, path: str) -> None:
        response = self.client.get(path)

        self.assertEqual("200 OK", response.status, response.data)
        self.assertEqual("application/json", response.mimetype)
        self.assertIsNotNone(response.json)
        self.assertIn("count", response.json)
        self.assertIn("results", response.json)
        self.assertEqual(response.json["count"], len(response.json["results"]))
