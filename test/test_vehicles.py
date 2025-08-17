import unittest

from ddt import ddt, data, unpack
from flask_server import app

from sample_data.payloads import (
    bike_gears_and_type_and_year,
    car_colours,
    car_make_and_year,
    car_less_than_or_equal_seats, 
    spaceship_singular_model,
    spaceship_two_models,
    spaceship_manufacturer_and_year
)


@ddt
class VehiclesTest(unittest.TestCase):
    spaceship_path: str = "/api/v1/vehicles/spaceships"
    car_path: str = "/api/v1/vehicles/cars"
    bike_path: str = "/api/v1/vehicles/bikes"

    def setUp(self) -> None:
        self.client = app.test_client()

        return super().setUp()

    @data(
        spaceship_path,
        car_path,
        bike_path,
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
        spaceship_path,
        car_path,
        bike_path,
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
        spaceship_path,
        car_path,
        bike_path,
    )
    def test_all_results(self, path: str) -> None:
        response = self.client.get(path)
        self.__assert_response_schema(response)

    @data(
        (spaceship_path, "top_speed", "DESC"),
        (spaceship_path, "top_speed", "ASC"),
        (spaceship_path, "max_crew", "DESC"),
        (spaceship_path, "max_crew", "ASC"),
        (car_path, "engine_size", "DESC"),
        (car_path, "engine_size", "ASC"),
        (car_path, "top_speed", "DESC"),
        (car_path, "top_speed", "ASC"),
        (bike_path, "wheel_size", "DESC"),
        (bike_path, "wheel_size", "ASC"),
        (bike_path, "gears", "DESC"),
        (bike_path, "gears", "ASC"),
    )
    @unpack
    def test_sorting(self, path: str, sort_field: str, sort_order: str) -> None:
        response = self.client.get(path, query_string=f"sort_field={sort_field}&sort_order={sort_order}")
        self.__assert_response_schema(response)
        prev = response.json["results"][0]
        for result in response.json["results"][1:]:
            if sort_order == "DESC":
                self.assertLessEqual(result[sort_field], prev[sort_field])
            elif sort_order == "ASC":
                self.assertGreaterEqual(result[sort_field], prev[sort_field])

    def test_spaceship_example_payloads(self) -> None:
        singular_response = self.client.get(self.spaceship_path, query_string=f"query={spaceship_singular_model.strip()}")
        self.__assert_response_schema(singular_response)

        self.assertEqual(1, singular_response.json["count"])
        for result in singular_response.json["results"]:
            self.assertEqual("Stardust Seeker", result["model"])
        
        two_models_response = self.client.get(self.spaceship_path, query_string=f"query={spaceship_two_models.strip()}")
        self.__assert_response_schema(two_models_response)

        self.assertEqual(2, two_models_response.json["count"])
        for result in two_models_response.json["results"]:
            self.assertTrue(result["model"] == "Nebula Rider" or result["model"] == "Stardust Seeker")
        
        manufacturer_and_year_response = self.client.get(self.spaceship_path, query_string=f"query={spaceship_manufacturer_and_year.strip()}")
        self.__assert_response_schema(manufacturer_and_year_response)

        self.assertEqual(1, manufacturer_and_year_response.json["count"])
        for result in manufacturer_and_year_response.json["results"]:
            self.assertEqual("AetherForge", result["manufacturer"])
            self.assertGreater(result["year"], 2010)

    def test_car_example_payloads(self) -> None:
        seats_response = self.client.get(self.car_path, query_string=f"query={car_less_than_or_equal_seats.strip()}")
        self.__assert_response_schema(seats_response)

        for result in seats_response.json["results"]:
            self.assertLessEqual(result["seats"], 7)
        
        colours_response = self.client.get(self.car_path, query_string=f"query={car_colours.strip()}")
        self.__assert_response_schema(colours_response)

        for result in colours_response.json["results"]:
            self.assertTrue(result["colour"].startswith("Light"))
            # .lower() here as the DB is not case sensitive
            self.assertIn("y", result["colour"].lower())
        
        make_and_year_response = self.client.get(self.car_path, query_string=f"query={car_make_and_year.strip()}")
        self.__assert_response_schema(make_and_year_response)

        for result in make_and_year_response.json["results"]:
            self.assertTrue(result["make"].endswith("s"))
            self.assertIn(result["year"], [1971, 2002])

    def test_bike_example_payloads(self) -> None:
        response = self.client.get(self.bike_path, query_string=f"query={bike_gears_and_type_and_year.strip()}")
        self.__assert_response_schema(response)

        for result in response.json["results"]:
            self.assertGreater(result["gears"], 3)
            self.assertNotIn(result["type"], ["BMX", "Road"])
            self.assertIn(result["year"], [2023, 2014])

    def __assert_response_schema(self, response) -> None:
        self.assertEqual("200 OK", response.status, response.data)
        self.assertEqual("application/json", response.mimetype)
        self.assertIsNotNone(response.json)
        self.assertIn("count", response.json)
        self.assertIn("results", response.json)
        self.assertEqual(response.json["count"], len(response.json["results"]))