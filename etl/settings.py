import os

POSTGRES_SETTINGS = {
    'dbname': os.getenv('POSTGRES_DB', 'movies_database'),
    'user': os.getenv('POSTGRES_USER', 'app'),
    'password': os.getenv('POSTGRES_PASSWORD', '123qwe'),
    'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

ETL_TRANSFER_PERIOD = os.environ.get('ETL_TRANSFER_PERIOD', 5)
