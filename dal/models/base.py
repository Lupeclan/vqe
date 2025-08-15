from abc import abstractmethod


class Base:
    table_name: str
    alias: str

    @classmethod
    @abstractmethod
    def get_create_table(cls) -> str:
        raise NotImplementedError
