from db_dataclasses import DataClassesStorage


class DataSerializer:
    """Сериалайзер для преобразования данных из sqlite к формату
     заполнения postgres

     """

    def __init__(self):
        self.result = {}
        self.prepare_dataclasses()

    def serialize(self, key: str, data: list):
        serialised = []
        key = self.prepare_key(key)
        for data_row in data:
            self.handle_data_values(data_row)
            serialised.append(self.result[key](**data_row))
        return serialised

    @classmethod
    def prepare_key(cls, key: str):
        return key.replace('_', '')

    def prepare_dataclasses(self):
        sub_classes = DataClassesStorage.__subclasses__()
        for class_ in sub_classes:
            self.result[class_.__name__.lower()] = class_

    @staticmethod
    def handle_data_values(data_row: dict):
        for key_, value in data_row.items():
            if not value:
                continue

            if isinstance(value, str) and "'" in value:
                data_row[key_] = value.replace("'", "''")
