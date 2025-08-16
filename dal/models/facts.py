from dal.models.base import Base
from dal.models.dimensions import Manufacturer, Model


class Car(Base):
    table_name: str = "fact_vehicle_cars"
    alias: str = "vhlc"
    primary_key: str = "car_id"
    query_columns: list[str] = (
        [
            "colour",
            "engine_size",
            "horsepower",
            "seats",
            "top_speed",
            "year",
        ]
        + Manufacturer.query_columns
        + Model.query_columns
    )

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `{cls.primary_key}` MEDIUMINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `{Manufacturer.primary_key}` SMALLINT UNSIGNED NOT NULL,
            `{Model.primary_key}` SMALLINT UNSIGNED NOT NULL,
            `colour` VARCHAR(64) NOT NULL,
            `engine_size` DECIMAL(2,1) NOT NULL DEFAULT 0,
            `horsepower` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
            `seats` TINYINT UNSIGNED NOT NULL DEFAULT 0,
            `top_speed` DECIMAL(5,1) UNSIGNED NOT NULL DEFAULT 0,
            `year` SMALLINT UNSIGNED NOT NULL,
            `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            `modified_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`{cls.primary_key}`),
            UNIQUE KEY (
                `{Manufacturer.primary_key}`,
                `{Model.primary_key}`,
                `colour`,
                `engine_size`,
                `horsepower`,
                `seats`,
                `top_speed`,
                `year`
            ),
            INDEX (`colour`),
            INDEX (`engine_size`),
            INDEX (`horsepower`),
            INDEX (`seats`),
            INDEX (`top_speed`),
            INDEX (`year`),
            CONSTRAINT `{cls.alias}_FK_{Manufacturer.primary_key}`
                FOREIGN KEY (`{Manufacturer.primary_key}`)
                REFERENCES `{Manufacturer.table_name}` (`{Manufacturer.primary_key}`),
            CONSTRAINT `{cls.alias}_FK_{Model.primary_key}`
                FOREIGN KEY (`{Model.primary_key}`)
                REFERENCES `{Model.table_name}` (`{Model.primary_key}`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""


class Bike(Base):
    table_name: str = "fact_vehicle_bikes"
    alias: str = "vhlb"
    primary_key: str = "bike_id"
    query_columns: list[str] = (
        [
            "gears",
            "type",
            "wheel_size",
            "year",
        ]
        + Manufacturer.query_columns
        + Model.query_columns
    )

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `{cls.primary_key}` MEDIUMINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `{Manufacturer.primary_key}` SMALLINT UNSIGNED NOT NULL,
            `{Model.primary_key}` SMALLINT UNSIGNED NOT NULL,
            `gears` TINYINT UNSIGNED NOT NULL,
            `type` ENUM('Road', 'BMX', 'City', 'Mountain', 'Hybrid') NOT NULL,
            `wheel_size` DECIMAL(3,1) UNSIGNED NOT NULL,
            `year` SMALLINT UNSIGNED NOT NULL,
            `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            `modified_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`{cls.primary_key}`),
            UNIQUE KEY (
                `{Manufacturer.primary_key}`,
                `{Model.primary_key}`,
                `gears`,
                `type`,
                `wheel_size`,
                `year`
            ),
            INDEX (`gears`),
            INDEX (`type`),
            INDEX (`wheel_size`),
            INDEX (`year`),
            CONSTRAINT `{cls.alias}_FK_{Manufacturer.primary_key}`
                FOREIGN KEY (`{Manufacturer.primary_key}`)
                REFERENCES `{Manufacturer.table_name}` (`{Manufacturer.primary_key}`),
            CONSTRAINT `{cls.alias}_FK_{Model.primary_key}`
                FOREIGN KEY (`{Model.primary_key}`)
                REFERENCES `{Model.table_name}` (`{Model.primary_key}`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""


class Spaceship(Base):
    table_name: str = "fact_vehicle_spaceships"
    alias: str = "vhls"
    primary_key: str = "spaceship_id"
    query_columns: list[str] = (
        [
            "max_crew",
            "top_speed",
            "year",
        ]
        + Manufacturer.query_columns
        + Model.query_columns
    )

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `{cls.primary_key}` MEDIUMINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `{Manufacturer.primary_key}` SMALLINT UNSIGNED NOT NULL,
            `{Model.primary_key}` SMALLINT UNSIGNED NOT NULL,
            `max_crew` SMALLINT UNSIGNED NOT NULL,
            `top_speed` DECIMAL(6,5) UNSIGNED NOT NULL,
            `year` SMALLINT UNSIGNED NOT NULL,
            `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            `modified_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`{cls.primary_key}`),
            UNIQUE KEY (
                `{Manufacturer.primary_key}`,
                `{Model.primary_key}`,
                `max_crew`,
                `top_speed`,
                `year`
            ),
            INDEX (`max_crew`),
            INDEX (`top_speed`),
            INDEX (`year`),
            CONSTRAINT `{cls.alias}_FK_{Manufacturer.primary_key}`
                FOREIGN KEY (`{Manufacturer.primary_key}`)
                REFERENCES `{Manufacturer.table_name}` (`{Manufacturer.primary_key}`),
            CONSTRAINT `{cls.alias}_FK_{Model.primary_key}`
                FOREIGN KEY (`{Model.primary_key}`)
                REFERENCES `{Model.table_name}` (`{Model.primary_key}`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""

    @classmethod
    def get_swagger_model(cls, api):
        from flask_restx import fields

        return api.model(
            cls.__name__,
            {
                "manufacturer": fields.String(
                    "Titan Galactic", description="Manufacturer of the spaceship."
                ),
                "max_crew": fields.Integer(400, description="Maximum crew capacity."),
                "model": fields.String(
                    "Star Wanderer", description="Model name of the spaceship."
                ),
                "top_speed": fields.String(
                    0.7098, description="Top speed as a fraction of light speed."
                ),
                "year": fields.Integer(
                    2025, description="Year the spaceship was manufactured."
                ),
            },
        )
