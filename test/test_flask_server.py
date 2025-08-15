import unittest

from flask_server import app


class FlaskServerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

        return super().setUp()

    def test_ping(self) -> None:
        response = self.client.get("/ping")

        self.assertEqual("200 OK", response.status)
        self.assertEqual(b"PONG", response.data)
        self.assertEqual("text/plain", response.mimetype)
