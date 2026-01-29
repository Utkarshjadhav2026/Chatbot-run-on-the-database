# db.py
# from agno.db.postgres import PostgresDb

# DATABASE_URL = (
#     "postgres//postgres:wemotive@1234@localhost:5432/mydatabase"
# )

# db = PostgresDb(
#     url=DATABASE_URL
# )

import psycopg2

DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "postgres",
    "password": "wemotive@1234",
    "host": "localhost",
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_url():
    db_url = "postgresql://postgres:wemotive%401234@localhost:5432/mydatabase"
    return db_url

