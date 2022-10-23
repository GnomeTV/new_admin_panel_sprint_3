import json
import logging
import os
import time
from contextlib import contextmanager
from urllib.parse import urljoin

import backoff
import psycopg2
import requests
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from requests.exceptions import ConnectionError

from settings import POSTGRES_SETTINGS, ETL_TRANSFER_PERIOD
from state_manager import State, JsonFileStorage


@contextmanager
def postgres_connect(dsl: dict, cursor_factory=None):
    connection = psycopg2.connect(**dsl)
    if cursor_factory:
        connection.cursor_factory = cursor_factory
    yield connection.cursor()
    connection.commit()
    connection.close()


class PostgresGetter:

    def __init__(self, state_file_path):
        self.state = State(JsonFileStorage(state_file_path))
        self.modified = None

    @staticmethod
    def prepare_ids_query(ids):
        return ', '.join([f"'{item[0]}'" for item in ids])

    def get_movies_data(self):
        modified = self.state.get_state('time')

        with postgres_connect(POSTGRES_SETTINGS, cursor_factory=DictCursor) \
                as cursor:
            query = """
                   SELECT
                       fw.id,
                       fw.title,
                       fw.description,
                       fw.rating,
                       fw.type,
                       fw.created,
                       fw.modified,
                       COALESCE (
                           json_agg(
                               DISTINCT jsonb_build_object(
                                   'person_role', pfw.role,
                                   'person_id', p.id,
                                   'person_name', p.full_name
                               )
                           ) FILTER (WHERE p.id is not null),
                           '[]'
                       ) as persons,
                       array_agg(DISTINCT g.name) as genres
                    FROM film_work fw
                    LEFT JOIN person_film_work pfw ON pfw.film_work_id = fw.id
                    LEFT JOIN person p ON p.id = pfw.person_id
                    LEFT JOIN genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN genre g ON g.id = gfw.genre_id
                    WHERE fw.modified > '{modified}'::timestamp OR
                     p.modified > '{modified}'::timestamp OR 
                     g.modified > '{modified}'::timestamp
                    GROUP BY fw.id
                    ORDER BY fw.modified
                    LIMIT 100;  
                    """.format(modified=modified)

            cursor.execute(query)
            result = cursor.fetchall()
        if not result:
            return []
        self.modified = result[-1]['modified'].strftime(self.state.date_format)
        self.state.set_state('time', self.modified)
        return result


class ElasticSetter:

    @staticmethod
    def compile_elastic_queue(result):
        result_query = ''
        for movie in result:
            movie_id = movie['id']
            directors = []
            actors_names = []
            actors = []
            writers_names = []
            writers = []
            for person in movie['persons']:
                role = person['person_role']
                name = person['person_name']
                id_ = person['person_id']

                if role == 'director':
                    directors.append(person['person_name'])

                if role == 'writer':
                    writers.append({'id': id_, 'name': name})
                    writers_names.append(person['person_name'])

                if role == 'actor':
                    actors.append({'id': id_, 'name': name})
                    actors_names.append(person['person_name'])

            result_query += json.dumps(
                {'index':
                    {
                        '_index': 'movies',
                        '_id': movie_id
                    }
                }
            ) + '\n' + json.dumps(
                {
                    'id': movie_id,
                    'imdb_rating': movie['rating'],
                    'genre': movie['genres'], 'title': movie['title'],
                    'description': movie['description'],
                    'director': directors,
                    'actors_names': actors_names,
                    'writers_names': writers_names,
                    'actors': actors, 'writers': writers
                }
            ) + '\n'

        return result_query

    @backoff.on_exception(backoff.expo, (OperationalError, ConnectionError),
                          max_tries=15)
    def set_data(self):
        data_getter = PostgresGetter(
            state_file_path=os.environ.get('STATE_FILEPATH')
        )
        while True:
            result = data_getter.get_movies_data()
            if not result:
                time.sleep(ETL_TRANSFER_PERIOD)
                continue
            queue = self.compile_elastic_queue(result)
            requests.post(url=urljoin(
                os.environ.get('ELK_HOST'), '_bulk'), data=queue,
                headers={
                    'Content-Type': 'application/x-ndjson'
                }
            )
            logging.info('Data transferred to Elastic!')


if __name__ == '__main__':
    ElasticSetter().set_data()
