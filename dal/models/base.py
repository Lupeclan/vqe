from abc import abstractmethod


class Base:
    table_name: str
    alias: str
    primary_key: str
    query_columns: list[str]

    @classmethod
    @abstractmethod
    def get_create_table(cls) -> str:
        raise NotImplementedError
