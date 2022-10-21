import os
import sqlite3

from dotenv import load_dotenv
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor

from data_transfer import PostgresSaver, SQLiteExtractor
from context_db_connections import sqlite_connect, postgres_connect

load_dotenv()


def load_from_sqlite(sqlite_cursor_: sqlite3.Cursor, pg_cursor_: _cursor):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_cursor_)
    sqlite_extractor = SQLiteExtractor(sqlite_cursor_)
    for data in sqlite_extractor.extract_movies_generator():
        postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('POSTGRES_DB', 'movies_database'),
        'user': os.getenv('POSTGRES_USER', 'app'),
        'password': os.getenv('POSTGRES_PASSWORD', '123qwe'),
        'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),
        'port': os.getenv('POSTGRES_PORT', 5432)}
    with sqlite_connect('db.sqlite', sqlite3.Row) \
            as sqlite_cursor, postgres_connect(dsl, cursor_factory=DictCursor)\
            as pg_cursor:
        load_from_sqlite(sqlite_cursor, pg_cursor)
