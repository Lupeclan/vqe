import unittest

from flask_server import app


class VehiclesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

        return super().setUp()

    def test_spaceships_invalid_query_json(self) -> None:
        response = self.client.get(
            "/api/v1/vehicles/spaceships",
            query_string='query={"model":{"operator":"and"}',
        )

        self.assertEqual("400 BAD REQUEST", response.status)
        self.assertEqual(b'{"error":"Invalid query supplied!"}\n', response.data)
        self.assertEqual("application/json", response.mimetype)

    def test_spaceships_all_results(self) -> None:
        response = self.client.get("/api/v1/vehicles/spaceships")

        self.assertEqual("200 OK", response.status, response.data)
        self.assertEqual("application/json", response.mimetype)
        self.assertIsNotNone(response.json)
        self.assertIn("count", response.json)
        self.assertIn("results", response.json)
        self.assertEqual(response.json["count"], len(response.json["results"]))
