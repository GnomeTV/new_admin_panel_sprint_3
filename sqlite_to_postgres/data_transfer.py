from typing import List

from data_serializer import DataSerializer
from db_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)


class BaseInserter:
    """Базовый класс, который управляет вставщиками в таблицы

    Args:
        key: Название таблицы в sqlite
        fields: Список полей таблицы в postgres
        insert_query: Шаблонная строка для вставки в

    """
    key: str = ''
    fields: list = []
    insert_query = "INSERT INTO {key} ({fields}) VALUES"

    @classmethod
    def handle_result_query(cls, result_query: str):
        result_query = result_query.replace("'None'", "NULL")
        return result_query[:-1] + ';'

    @classmethod
    def prepare_fields(cls):
        """Соединяет названия полей с разделителем"""
        return ', '.join(cls.fields)

    @classmethod
    def prepare_values_query(cls):
        """Создает шаблонную строку для заполнения значениями полей

            Returns:
                str: "\n('{field1}','{field2}','{field3}')"
        """
        query = ''
        result = []
        for field in cls.fields:
            result.append("'{" + field + "}'")
        query = '\n({}),'.format(', '.join(result))
        return query


class GenreInserter(BaseInserter):
    key = 'genre'
    fields = ['name', 'description', 'created', 'modified', 'id']

    @classmethod
    def prepare_genre_query(cls, genres: List[Genre]):
        result_query = cls.insert_query.format(key=cls.key,
                                               fields=cls.prepare_fields())
        for row in genres:
            result_query += cls.prepare_values_query().format(
                name=row.name,
                description=row.description,
                created=row.created_at,
                modified=row.updated_at,
                id=row.id)
        return cls.handle_result_query(result_query)


class PersonInserter(BaseInserter):
    key = 'person'
    fields = ['id', 'full_name', 'created', 'modified']

    @classmethod
    def prepare_person_query(cls, persons: List[Person]):
        result_query = cls.insert_query.format(key=cls.key,
                                               fields=cls.prepare_fields())
        for row in persons:
            result_query += cls.prepare_values_query().format(
                full_name=row.full_name,
                created=row.created_at,
                modified=row.updated_at,
                id=row.id)

        return cls.handle_result_query(result_query)


class FilmworkInserter(BaseInserter):
    key = 'film_work'
    fields = ['file_path', 'title', 'description', 'creation_date', 'type',
              'rating', 'created', 'modified', 'id']

    @classmethod
    def prepare_film_work_query(cls, film_works: List[Filmwork]):
        result_query = cls.insert_query.format(key=cls.key,
                                               fields=cls.prepare_fields())
        for row in film_works:
            result_query += cls.prepare_values_query().format(
                file_path=row.file_path,
                title=row.title,
                description=row.description,
                creation_date=row.creation_date,
                type=row.type,
                rating=row.rating,
                created=row.created_at,
                modified=row.updated_at,
                id=row.id)

        return cls.handle_result_query(result_query)


class GenreFilmworkInserter(BaseInserter):
    key = 'genre_film_work'
    fields = ['created', 'genre_id', 'film_work_id', 'id']

    @classmethod
    def prepare_genre_film_work_query(cls,
                                      genre_film_works: List[GenreFilmwork]):
        result_query = cls.insert_query.format(key=cls.key,
                                               fields=cls.prepare_fields())
        for row in genre_film_works:
            result_query += cls.prepare_values_query().format(
                created=row.created_at,
                genre_id=row.genre_id,
                film_work_id=row.film_work_id,
                id=row.id)

        return cls.handle_result_query(result_query)


class PersonFilmworkInserter(BaseInserter):
    key = 'person_film_work'
    fields = ['role', 'created', 'id', 'person_id', 'film_work_id']

    @classmethod
    def prepare_person_film_work_query(cls,
                                       person_film_work: List[PersonFilmwork]):
        result_query = cls.insert_query.format(key=cls.key,
                                               fields=cls.prepare_fields())
        for row in person_film_work:
            result_query += cls.prepare_values_query().format(
                role=row.role,
                created=row.created_at,
                id=row.id,
                film_work_id=row.film_work_id,
                person_id=row.person_id)

        return cls.handle_result_query(result_query)


class PostgresSaver:
    """Класс отвечающий за вставку значений в postgres

    Args:
        cursor: курсор управления postgres

    """

    def __init__(self, cursor):
        self.cursor = cursor

    def save_all_data(self, data: dict):
        self.insert_genre(data.get('genre'))
        self.insert_person(data.get('person'))
        self.insert_film_work(data.get('film_work'))
        self.insert_genre_film_work(data.get('genre_film_work'))
        self.insert_person_film_work(data.get('person_film_work'))

    def insert_genre(self, genres: List):
        if not genres:
            return
        serialised_data = DataSerializer().serialize('genre', genres)
        result_query = GenreInserter.prepare_genre_query(serialised_data)
        self.cursor.execute(result_query)

    def insert_person(self, persons: List):
        if not persons:
            return
        serialised_data = DataSerializer().serialize('person', persons)
        result_query = PersonInserter.prepare_person_query(serialised_data)
        self.cursor.execute(result_query)

    def insert_film_work(self, film_works: List):
        if not film_works:
            return
        serialised_data = DataSerializer().serialize('film_work', film_works)
        result_query = FilmworkInserter.prepare_film_work_query(
            serialised_data)
        self.cursor.execute(result_query)

    def insert_genre_film_work(self, genre_film_works: List):
        if not genre_film_works:
            return
        serialised_data = DataSerializer().serialize('genre_film_work',
                                                     genre_film_works)
        result_query = GenreFilmworkInserter.prepare_genre_film_work_query(
            serialised_data)
        self.cursor.execute(result_query)

    def insert_person_film_work(self, person_film_works: List):
        if not person_film_works:
            return
        serialised_data = DataSerializer().serialize('person_film_work',
                                                     person_film_works)
        result_query = PersonFilmworkInserter.prepare_person_film_work_query(
            serialised_data)
        self.cursor.execute(result_query)


class SQLiteExtractor:
    """Класс отвечающий за вставку значений в postgres

        Args:
            cursor: курсор управления sqlite

        """

    tables = ['genre', 'person', 'film_work', 'genre_film_work',
              'person_film_work', ]

    def __init__(self, cursor):
        self.cursor = cursor

    def extract_movies_generator(self) -> dict:
        """Достает данные из базы sqlite"""
        for table in self.tables:
            query = "SELECT * FROM {tablename}".format(tablename=table)
            self.cursor.execute(query)
            while True:
                query_result = self.cursor.fetchmany(5)
                if not query_result:
                    break
                yield {table: [dict(result) for result in query_result]}
