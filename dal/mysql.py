import logging
import json

from typing import Optional

from sqlalchemy import create_engine, text

# from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from dal.models.dimensions import Manufacturer, Model


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

        for cls in [Manufacturer, Model]:
            self.execute(cls.get_create_table())

        spaceships = self.__load_sample_data("spaceships.json")
        self.load_dimension(
            Manufacturer.table_name,
            ["manufacturer"],
            [":manufacturer"],
            spaceships,
        )

        self.load_dimension(
            Model.table_name,
            ["model"],
            [":model"],
            spaceships,
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

    def read_sql_query(self, query: str, params: Optional[dict] = None) -> dict:
        raw_results = {}
        with self.get_session() as session:
            if params is None:
                raw_results = session.connection().execute(text(query))
            else:
                raw_results = session.connection().execute(text(query), params)

        data = {}
        i = 0
        for row in raw_results:
            data[i] = row._asdict()
            i += 1

        return data

    def get_session(self):
        return Session(self.engine)

    def __load_sample_data(self, file_name: str) -> list[dict]:
        with open(f"/app/sample_data/{file_name}", encoding="utf-8") as f:
            # first item in list is schema description
            return json.load(f)[1:]
