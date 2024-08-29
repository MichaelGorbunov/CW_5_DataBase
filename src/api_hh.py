import os
from typing import Any

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()
db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
}


def get_employers_by_name(name: str, per_page: int = 20) -> list[dict[str, Any]]:
    """
    Функция для получения списка работодателей по имени с hh.ru.
    :param name: Имя работодателя для поиска.
    :param per_page: Количество работодателей на одной странице (по умолчанию 20).
    :return: Список работодателей.
    """
    url = "https://api.hh.ru/employers"
    params = {
        "text": name,
        "per_page": per_page,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    employers_data = response.json()
    # print(employers_data.get("items", []))
    return employers_data.get("items", [])


def get_employers_info(employer_id: int) -> list[dict[str, Any]]:
    """ """
    url = f"https://api.hh.ru/employers/{employer_id}"
    employer = []

    response = requests.get(url)
    response.raise_for_status()
    employers_data = response.json()
    # print(employers_data.get("description"))
    # print(employers_data.get("name"))
    # print(employers_data.get("site_url"))
    employer.append(
        {
            "company_id": employer_id,
            "company_name": employers_data.get("name"),
            "company_desc": employers_data.get("description"),
            "company_url": employers_data.get("site_url"),
        }
    )
    return employer


def get_vacancies_by_employer(
    employer_id: int, per_page: int = 20
) -> list[dict[str, Any]]:
    """
    Функция для получения списка вакансий работодателя с hh.ru.
    :param employer_id: ID работодателя.
    :param per_page: Количество вакансий на  странице (по умолчанию 20).
    :return: Список вакансий.
    """
    url = "https://api.hh.ru/vacancies"
    params = {
        "employer_id": employer_id,
        "per_page": per_page,
        "area": 113,  # Россия
        "only_with_salary": True,  # Указана зарплата
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    vacancies_data = response.json()

    # return vacancies_data.get("items", [])
    vacancies: list = []
    for vacans in vacancies_data.get("items", []):
        vacancies.append(
            {
                "vacancy_id": int(vacans.get("id")),
                "company_id": employer_id,
                "vacan_title": vacans.get("name"),
                "city": vacans.get("area").get("name"),
                # "salary_from": vacans.get("salary").get("from"),
                "salary_from": (
                    vacans.get("salary").get("from")
                    if vacans.get("salary").get("from") is not None
                    else 0
                ),
                # "salary_to": vacans.get("salary").get("to"),
                # "salary_to": (
                #     vacans.get("salary").get("to")
                #     if vacans.get("salary").get("to") is not None
                #     else 0
                # ),
                "vacancy_url": vacans.get("alternate_url"),
                "vacan_req": (
                    vacans.get("snippet").get("requirement")
                    if vacans.get("snippet").get("requirement") is not None
                    else "Не указано"
                ),
                "vacan_resp": (
                    vacans.get("snippet").get("responsibility")
                    if vacans.get("snippet").get("responsibility") is not None
                    else "Не указано"
                ),
            }
        )
    return vacancies


def insert_emp_data(emp_id:int):
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:

        company = get_vacancies_by_employer(emp_id)
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
        )

    conn.commit()
    conn.close()


def insert_vac_data(emp_id:int):
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cur:

        vacancy = get_vacancies_by_employer(emp_id,5)
        for item in vacancy:

            vacancy_id = item.get("vacancy_id")
            company_id = item.get("company_id")
            vacan_title = item.get("vacan_title")
            city = item.get("city")
            salary_from = item.get("salary_from")
            vacancy_url = item.get("vacancy_url")
            vacan_req = item.get("vacan_req")
            vacan_resp = item.get("vacan_resp")
            # print(vacancy_id,
            #     company_id,
            #     vacan_title,
            #     city ,
            #     salary_from,
            #     vacancy_url,
            #     vacan_req,
            #     vacan_resp)

            cur.execute(
                f"""MERGE INTO vacancies USING (VALUES({vacancy_id})) as src(id)
                ON vacancies.vacancy_id = src.id
                WHEN NOT MATCHED
                THEN INSERT VALUES({vacancy_id}, {company_id}, '{vacan_title}', '{city}', 
                {salary_from}, '{vacancy_url}', '{vacan_req}', '{vacan_resp}');"""
            )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # main()
    # get_employers_by_name('МТС',100)
    # print(get_vacancies_by_employer(3529, 100))
    # print(get_employers_info(6040))

    # for item in [6041,2227671,2748,3776,3529,78638,4233,5390761,2180,906557]:
    #     get_employers_info(item)

    # for item in [6041, 2227671, 2748, 3776, 3529, 78638, 4233, 5390761, 2180, 906557]:
    #     print(get_employers_info(item))
    #     vacan=get_vacancies_by_employer(item,15)
    #     for item in vacan:
    #         print(item)

    # insert_emp_data()

    # for item in [6041, 2227671, 2748, 3776, 3529, 78638, 4233, 5390761, 2180, 906557]:
    #     insert_emp_data(item)

    for item in [6041, 2227671, 2748, 3776, 3529, 78638, 4233, 5390761, 2180, 906557]:
        insert_vac_data(item)
