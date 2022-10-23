import abc
import json
from datetime import datetime
from typing import Any, Optional


class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w+') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r+') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            self.save_state({})
            return {}


class State:
    date_format = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        data = self.storage.retrieve_state()
        return data.get(key, datetime(year=2000, day=28, month=10).strftime(
            self.date_format))
