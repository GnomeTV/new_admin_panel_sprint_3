import sqlite3
from contextlib import contextmanager

import psycopg2


@contextmanager
def sqlite_connect(db_path: str, row_factory=None):
    connection = sqlite3.connect(db_path)
    if row_factory:
        connection.row_factory = row_factory
    yield connection.cursor()
    connection.commit()
    connection.close()


@contextmanager
def postgres_connect(dsl: dict, cursor_factory=None):
    connection = psycopg2.connect(**dsl)
    if cursor_factory:
        connection.cursor_factory = cursor_factory
    yield connection.cursor()
    connection.commit()
    connection.close()
