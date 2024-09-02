import os
from typing import Any, List, Tuple

import psycopg2
from dotenv import load_dotenv
from src.api_hh import get_employers_info,get_vacancies_by_employer

load_dotenv()
db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
}
db_config_first_conn = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB_FIRST_CONN"),
}


def create_tables() -> None:
    """функция создания таблиц"""
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR NOT NULL,
                company_desc TEXT,
                company_url TEXT                
                );
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
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
        """
        )
    conn.commit()
    conn.close()


def create_db():
    """функция создания базы данных"""
    conn = psycopg2.connect(**db_config_first_conn)
    cursor = conn.cursor()
    conn.autocommit = True

    sql_qr = f"CREATE DATABASE {db_config['dbname']}"
    cursor.execute(sql_qr)
    print("База данных успешно создана")
    cursor.close()
    conn.close()

def check_db() -> bool:
    """функция проверяет наличие базы данных """
    with psycopg2.connect(**db_config_first_conn) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT count(datname) FROM pg_database WHERE datname = (%s) ",
            (db_config["dbname"],),
        )
        rows = cur.fetchall()
        cur.close()


        if rows[0][0] != 1:
            return False
        else:
            return True
        conn.close()

def insert_emp_data(emp_id: int):
    """Функция всавки в базу информации об работодателе по emp_id  """
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:
        company = get_employers_info(emp_id)
        company_id = company[0].get("company_id")
        company_name = company[0].get("company_name")
        company_desc = company[0].get("company_desc")
        company_url = company[0].get("company_url")
        # print(company[0].get('company_id'))
        # print(company_id,company_name)

        # cur.execute("""
        #                 INSERT INTO companies (company_id, company_name, company_desc,company_url)
        #                 VALUES (%s, %s, %s, %s);
        #             """, (company_id, company_name, company_desc,company_url))
        cur.execute(
            f"""MERGE INTO companies USING (VALUES({company_id})) as src(id)
        ON companies.company_id = src.id
        WHEN NOT MATCHED
        THEN INSERT VALUES({company_id}, '{company_name}', '{company_desc}', '{company_url}');"""
        )#предотвращение конфликтов при вставке одинаковых данных

    conn.commit()
    conn.close()

def insert_vac_data(emp_id: int, count: int):
    """функция вставки в базу данных о вакансиях
    emp_id: id работодателя
    count: int количество вакансий"""
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:
        vacancy = get_vacancies_by_employer(emp_id, count)
        # print(vacancy)
        if vacancy is None:
            print("err get_vacancies_by_employer ")


        for item in vacancy:
            vacancy_id = item.get("vacancy_id")
            company_id = item.get("company_id")
            vacan_title = item.get("vacan_title")
            city = item.get("city")
            salary_from = item.get("salary_from")
            vacancy_url = item.get("vacancy_url")
            vacan_req = item.get("vacan_req")
            vacan_resp = item.get("vacan_resp")

            # cur.execute(
            #     f"""MERGE INTO vacancies USING (VALUES({vacancy_id})) as src(id)
            #     ON vacancies.vacancy_id = src.id
            #     WHEN NOT MATCHED
            #     THEN INSERT VALUES({vacancy_id}, {company_id}, '{vacan_title}', '{city}',
            #     {salary_from}, '{vacancy_url}', '{vacan_req}', '{vacan_resp}');"""
            # )
            cur.execute(
                f"""
            INSERT     INTO vacancies(vacancy_id, company_id,vacan_title,city,salary_from,vacancy_url,vacan_req,vacan_resp) 
            VALUES({vacancy_id}, {company_id}, '{vacan_title}', '{city}',{salary_from}, '{vacancy_url}', '{vacan_req}', '{vacan_resp}')
            ON CONFLICT(vacancy_id)DO NOTHING;""")

    conn.commit()
    conn.close()

# create_tables()
