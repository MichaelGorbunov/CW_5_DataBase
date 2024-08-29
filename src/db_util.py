import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()
db_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}
def create_tables() -> None:
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR NOT NULL,
                company_desc TEXT,
                company_url TEXT                
                --open_vacancies INTEGER
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(company_id),
                vacan_title TEXT NOT NULL,
                city VARCHAR,  
                salary_from INTEGER,
                vacancy_url TEXT,
                vacan_req TEXT,
                vacan_resp TEXT
            );
        """)
    conn.commit()
    conn.close()
def create_db():
    conn = psycopg2.connect(database='postgres', user=os.getenv('POSTGRES_USER'),
                            password=os.getenv('POSTGRES_PASSWORD'),
                            host=os.getenv('POSTGRES_HOST'),
                            port=os.getenv('POSTGRES_PORT'))
    cursor = conn.cursor()
    conn.autocommit = True

    sql_qr = f"CREATE DATABASE {db_config['dbname']}"
    cursor.execute(sql_qr)
    print("База данных успешно создана")
    cursor.close()
    conn.close()


create_tables()