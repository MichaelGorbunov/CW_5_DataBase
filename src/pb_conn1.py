import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
}
# print(db_config['dbname'])


def create_db():
    conn = psycopg2.connect(
        database="postgres",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    cursor = conn.cursor()
    conn.autocommit = True

    sql_qr = f"CREATE DATABASE {db_config['dbname']}"
    cursor.execute(sql_qr)
    print("База данных успешно создана")
    cursor.close()
    conn.close()


with psycopg2.connect(
    database="postgres",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
) as conn:
    cur = conn.cursor()

    cur.execute(
        "SELECT count(datname) FROM pg_database WHERE datname = (%s) ",
        (db_config["dbname"],),
    )
    rows = cur.fetchall()
    cur.close()

    if rows[0][0] != 1:
        print("база не создана")
        create_db()

    # conn.commit()

conn.close()
