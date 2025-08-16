import logging
import json

from typing import Optional

from sqlalchemy import create_engine, text

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from dal.models.base import Base
from dal.models.dimensions import Manufacturer, Model
from dal.models.facts import Car, Bike, Spaceship


class MySQLDal:
    engine: Engine
    db_name: str = "vqe"

    def __init__(self) -> None:
        logging.info("Creating engine...")
        self.engine = create_engine(
            f"mysql+pymysql://root:root@db:3306",
            pool_size=2,
            max_overflow=8,
            pool_pre_ping=True,
            pool_recycle=1800,
        )

    def scaffold(self):
        if self.database_exists(self.db_name):
            logging.info(f"{self.db_name} already exists, skipping scaffold...")
            return

        logging.info(f"Scaffolding database {self.db_name}...")
        self.execute(f"CREATE DATABASE `{self.db_name}`")

        for cls in [Manufacturer, Model, Car, Bike, Spaceship]:
            self.execute(cls.get_create_table())

        self.load_spaceships()
        self.load_bikes()
        self.load_cars()

    def load_spaceships(self) -> None:
        logging.info("Loading Spaceships...")
        spaceships = self.__load_sample_data("spaceships.json")
        self.load_manufacturers(spaceships, ":manufacturer")
        self.load_models(spaceships)

        query = f"""INSERT INTO `{self.db_name}`.`{Spaceship.table_name}`
            (
               `{Manufacturer.primary_key}`,
               `{Model.primary_key}`,
               `max_crew`,
               `top_speed`,
               `year`
            )
            SELECT
                (
                    SELECT `{Manufacturer.primary_key}` FROM `{self.db_name}`.`{Manufacturer.table_name}`
                    WHERE `manufacturer` = :manufacturer
                ) AS {Manufacturer.primary_key!r},
                (
                    SELECT `{Model.primary_key}` FROM `{self.db_name}`.`{Model.table_name}`
                    WHERE `model` = :model
                ) AS {Model.primary_key!r},
                :max_crew,
                :top_speed,
                :year
        """

        self.execute_many(query, spaceships)

    def load_bikes(self) -> None:
        logging.info("Loading Bikes...")
        bikes = self.__load_sample_data("bikes.json")
        self.load_manufacturers(bikes, ":brand")
        self.load_models(bikes)

        query = f"""INSERT INTO `{self.db_name}`.`{Bike.table_name}`
            (
               `{Manufacturer.primary_key}`,
               `{Model.primary_key}`,
               `gears`,
               `type`,
               `wheel_size`,
               `year`
            )
            SELECT
                (
                    SELECT `{Manufacturer.primary_key}` FROM `{self.db_name}`.`{Manufacturer.table_name}`
                    WHERE `manufacturer` = :brand
                ) AS {Manufacturer.primary_key!r},
                (
                    SELECT `{Model.primary_key}` FROM `{self.db_name}`.`{Model.table_name}`
                    WHERE `model` = :model
                ) AS {Model.primary_key!r},
                :gears,
                :type,
                :wheel_size,
                :year
        """

        self.execute_many(query, bikes)

    def load_cars(self) -> None:
        logging.info("Loading Cars...")
        cars = self.__load_sample_data("cars.json")
        self.load_manufacturers(cars, ":make")
        self.load_models(cars)

        query = f"""INSERT INTO `{self.db_name}`.`{Car.table_name}`
            (
               `{Manufacturer.primary_key}`,
               `{Model.primary_key}`,
               `colour`,
               `engine_size`,
               `horsepower`,
               `seats`,
               `top_speed`,
               `year`
            )
            SELECT
                (
                    SELECT `{Manufacturer.primary_key}` FROM `{self.db_name}`.`{Manufacturer.table_name}`
                    WHERE `manufacturer` = :make
                ) AS {Manufacturer.primary_key!r},
                (
                    SELECT `{Model.primary_key}` FROM `{self.db_name}`.`{Model.table_name}`
                    WHERE `model` = :model
                ) AS {Model.primary_key!r},
                :colour,
                :engine_size,
                :horsepower,
                :seats,
                :top_speed,
                :year
        """

        self.execute_many(query, cars)

    def load_models(self, data: list[dict]) -> int:
        return self.load_dimension(
            Model.table_name,
            ["model"],
            [":model"],
            data,
        )

    def load_manufacturers(self, data: list[dict], param_name: str) -> int:
        return self.load_dimension(
            Manufacturer.table_name,
            ["manufacturer"],
            [param_name],
            data,
        )

    def load_dimension(
        self, table_name: str, columns: list[str], params: list[str], data: list[dict]
    ) -> int:
        columns_part = "`,`".join(columns)
        values_part = ",".join(params)
        rows = self.execute_many(
            f"INSERT IGNORE INTO `{self.db_name}`.`{table_name}` ({columns_part}) VALUES ({values_part});",
            data,
        )

        logging.info(f"Loaded {rows} into {table_name}")
        return rows

    def query(
        self,
        cls: Base,
        query: Optional[dict] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> dict:
        columns = "`,`".join(cls.query_columns)
        query_string = f"""
            SELECT
                `{columns}`,
                {Manufacturer.alias}.`manufacturer`,
                {Model.alias}.`model`
            FROM `{self.db_name}`.`{cls.table_name}` {cls.alias}
            JOIN `{self.db_name}`.`{Manufacturer.table_name}` {Manufacturer.alias}
                USING (`{Manufacturer.primary_key}`)
            JOIN `{self.db_name}`.`{Model.table_name}` {Model.alias}
                USING (`{Model.primary_key}`)
        """

        params = {}
        if query:
            logging.info(query)
            parts = []

            for column_name, column_value in query.items():
                if (
                    "constraints" not in column_value
                    or len(column_value["constraints"]) < 1
                ):
                    continue

                op = column_value["operator"]
                i = 0
                inner_parts = []
                for constraint in column_value["constraints"]:
                    value = constraint["value"]
                    param = f":arg_{column_name}_{i}"
                    if constraint["operator"] == "equals":
                        inner_parts.append(f"`{column_name}` = {param}")
                    elif constraint["operator"] == "notEquals":
                        inner_parts.append(f"`{column_name}` != {param}")
                    elif constraint["operator"] == "startsWith":
                        inner_parts.append(f"`{column_name}` LIKE {param}")
                        value = f"{constraint['value']}%"
                    elif constraint["operator"] == "endsWith":
                        inner_parts.append(f"`{column_name}` LIKE {param}")
                        value = f"%{constraint['value']}"
                    elif constraint["operator"] == "contains":
                        inner_parts.append(f"`{column_name}` LIKE {param}")
                        value = f"%{constraint['value']}%"
                    elif constraint["operator"] == "notContains":
                        inner_parts.append(f"`{column_name}` NOT LIKE {param}")
                        value = f"%{constraint['value']}%"
                    elif constraint["operator"] == "lt":
                        inner_parts.append(f"`{column_name}` < {param}")
                    elif constraint["operator"] == "lte":
                        inner_parts.append(f"`{column_name}` <= {param}")
                    elif constraint["operator"] == "gt":
                        inner_parts.append(f"`{column_name}` > {param}")
                    elif constraint["operator"] == "gte":
                        inner_parts.append(f"`{column_name}` >= {param}")
                    elif constraint["operator"] == "in":
                        inner_parts.append(f"`{column_name}` IN {param}")
                        if type(value) is not list:
                            value = [value]
                    elif constraint["operator"] == "notIn":
                        inner_parts.append(f"`{column_name}` NOT IN {param}")
                        if type(value) is not list:
                            value = [value]
                    params[param[1:]] = value
                    i += 1

                parts.append(f"({f' {op} '.join(inner_parts)})")

            if parts and len(parts) > 0:
                query_string += f" WHERE ({f' AND '.join(parts)})"

        if sort_field and sort_order:
            query_string += f" ORDER BY `{sort_field}` {sort_order}"

        logging.info(query_string)
        logging.info(params)
        return self.read_sql_query(query_string, params)

    def database_exists(self, db_name: str) -> bool:
        query_string = f"SELECT `SCHEMA_NAME` FROM `INFORMATION_SCHEMA`.`SCHEMATA` WHERE `SCHEMA_NAME` = :db_name"
        result = self.read_sql_query(query_string, {"db_name": db_name})
        if result is None or not result or len(result) < 1:
            return False
        return True

    def execute(
        self, query: str, params: Optional[dict] = None, return_row_id: bool = False
    ) -> int:
        with self.get_session() as session:
            result = session.connection().execute(text(query), params)
            session.commit()
            return result.lastrowid if return_row_id else result.rowcount

    def execute_many(self, query: str, params: list[dict]) -> int:
        rows = 0
        with self.get_session() as session:
            for p in params:
                result = session.connection().execute(text(query), p)
                rows += result.rowcount
            session.commit()

        return rows

    def read_sql_query(self, query: str, params: Optional[dict] = None) -> list:
        raw_results = {}
        with self.get_session() as session:
            if params is None:
                raw_results = session.connection().execute(text(query))
            else:
                raw_results = session.connection().execute(text(query), params)

        data = []
        for row in raw_results:
            data.append(row._asdict())

        return data

    def get_session(self):
        return Session(self.engine)

    def __load_sample_data(self, file_name: str) -> list[dict]:
        with open(f"/app/sample_data/{file_name}", encoding="utf-8") as f:
            # first item in list is schema description
            return json.load(f)[1:]
