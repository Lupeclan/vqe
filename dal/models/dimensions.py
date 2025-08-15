from dal.models.base import Base


class Manufacturer(Base):
    table_name: str = "dim_manufacturers"
    alias: str = "manu"
    primary_key: str = "manufacturer_id"

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `{cls.primary_key}` SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `manufacturer` VARCHAR(128) NOT NULL,
            `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            `modified_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`{cls.primary_key}`),
            UNIQUE KEY (`manufacturer`),
            INDEX (`manufacturer`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""


class Model(Base):
    table_name: str = "dim_models"
    alias: str = "mdl"
    primary_key: str = "model_id"

    @classmethod
    def get_create_table(cls) -> str:
        return f"""CREATE TABLE IF NOT EXISTS `vqe`.`{cls.table_name}` (
            `{cls.primary_key}` SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            `model` VARCHAR(128) NOT NULL,
            `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            `modified_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`{cls.primary_key}`),
            UNIQUE KEY (`model`),
            INDEX (`model`)
        )
        ENGINE = INNODB
        AUTO_INCREMENT = 0;"""
