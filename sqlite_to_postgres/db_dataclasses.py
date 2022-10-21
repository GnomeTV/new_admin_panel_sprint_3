import uuid
from dataclasses import dataclass, field


class DataClassesStorage:
    pass


@dataclass
class Filmwork(DataClassesStorage):
    file_path: str
    title: str
    description: str
    creation_date: str
    type: type
    rating: field(default=0.0)
    created_at: str
    updated_at: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person(DataClassesStorage):
    full_name: str
    created_at: str
    updated_at: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre(DataClassesStorage):
    name: str
    description: str
    created_at: str
    updated_at: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmwork(DataClassesStorage):
    role: str
    created_at: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmwork(DataClassesStorage):
    created_at: str
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
