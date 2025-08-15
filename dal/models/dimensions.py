from dal.models.base import Base


class Manufacturer(Base):
    table_name: str = "dim_manufacturers"
    alias: str = "manu"

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `manufacturer_id` SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `manufacturer` VARCHAR(128) NOT NULL,
            PRIMARY KEY (`manufacturer_id`),
            UNIQUE KEY (`manufacturer`),
            INDEX (`manufacturer`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""


class Model(Base):
    table_name: str = "dim_models"
    alias: str = "mod"

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `model_id` SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `model` VARCHAR(128) NOT NULL,
            PRIMARY KEY (`model_id`),
            UNIQUE KEY (`model`),
            INDEX (`model`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""
