import os

from dotenv import load_dotenv

from context_db_connections import postgres_connect, sqlite_connect

load_dotenv()


class DBExtractor:
    tables_list = ['genre', 'person', 'film_work', 'person_film_work',
                   'genre_film_work']

    def get_rows_count(self):
        pass

    def get_rows_content(self):
        pass

    @staticmethod
    def row_count(table, cursor):
        cursor.execute("select count(*) from {table}".format(table=table))
        query_result = cursor.fetchall()
        return query_result

    @staticmethod
    def row_content(table, cursor):
        query = "SELECT id FROM {table}".format(table=table)
        cursor.execute(query)
        query_result = cursor.fetchall()
        return query_result


class PostgresTester(DBExtractor):
    db_setting = {
        'dbname': os.getenv('DB_NAME', 'postgres'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres'),
        'host': '127.0.0.1',
        'port': os.getenv('DB_PORT', 5432)}

    @classmethod
    def get_rows_count(cls):
        postgres_row_count = {}
        with postgres_connect(cls.db_setting) as cursor:
            for table in cls.tables_list:
                postgres_row_count[table] = cls.row_count(table, cursor)[0][0]
        return postgres_row_count

    @classmethod
    def get_rows_content(cls):
        postgres_row_result = {}
        with postgres_connect(cls.db_setting) as cursor:
            for table in cls.tables_list:
                postgres_row_result[table] = [item[0] for item in
                                              cls.row_content(table,
                                                              cursor)].sort()
        return postgres_row_result


class SqliteTester(DBExtractor):
    db_settings = '../../sqlite_to_postgres/db.sqlite'

    @classmethod
    def get_rows_count(cls):
        sqlite_row_count = {}
        with sqlite_connect(cls.db_settings,
                            lambda cursor_, row: row[0]) as cursor:
            for table in cls.tables_list:
                sqlite_row_count[table] = cls.row_count(table, cursor)[0]
        return sqlite_row_count

    @classmethod
    def get_rows_content(cls):
        sqlite_row_result = {}
        with sqlite_connect(cls.db_settings,
                            lambda cursor_, row: row[0]) as cursor:
            for table in cls.tables_list:
                sqlite_row_result[table] = cls.row_content(table,
                                                           cursor).sort()
        return sqlite_row_result


def test_count_rows():
    postgres_result = PostgresTester().get_rows_count()
    sqlite_result = SqliteTester().get_rows_count()
    assert postgres_result == sqlite_result


def test_rows_content():
    postgres_result = PostgresTester.get_rows_content()
    sqlite_result = SqliteTester.get_rows_content()
    assert postgres_result == sqlite_result
