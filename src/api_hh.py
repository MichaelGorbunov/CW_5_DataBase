# import os
# import time
from typing import Any

import requests

# start_time = time.time()


def get_employers_by_name(name: str, per_page: int = 100) -> list[dict[str, Any]]:
    """
    Функция для получения списка работодателей по имени с hh.ru.
    :param name: Имя работодателя для поиска.
    :param per_page: Количество работодателей на одной странице (по умолчанию 100).
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
    """Функция получения информации о работодателе
    по его employer_id"""
    url = f"https://api.hh.ru/employers/{employer_id}"
    employer = []
    response = requests.get(url)
    response.raise_for_status()
    employers_data = response.json()
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
    employer_id: int, per_page: int = 100
) -> list[dict[str, Any]]:
    """
    Функция для получения списка вакансий работодателя с hh.ru.
    :param employer_id: ID работодателя.
    :param per_page: Количество вакансий на  странице (по умолчанию 100).
    :return: Список вакансий.
    """
    url = "https://api.hh.ru/vacancies"
    params = {
        "employer_id": employer_id,
        "per_page": per_page,
        "area": 113,  # Россия
        "only_with_salary": True,  # Указана зарплата
        "page": 0,
    }
    vacancies: list = []

    session = requests.session()

    for page in range(20):
        params["page"] = page
        response = session.get(url, params=params)
        response.raise_for_status()

        if response.status_code != 200:
            session.close()
            return vacancies

        vacancies_data = response.json()

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

        if vacancies_data.get("page") == vacancies_data.get("pages"):
            session.close()
            return vacancies
    session.close()
    return vacancies


if __name__ == "__main__":
    print("api_hh")
    # main()
    # get_employers_by_name('МТС',100)
    # for item in [6041,3776]:
    #     vacan = get_vacancies_by_employer(item, 100)
    #     for item in vacan:
    #         print(item)
    # print("--- %s seconds ---" % (time.time() - start_time))
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

    # for item in [6041, 2227671, 2748, 3776, 3529, 78638, 4233, 5390761, 2180, 906557]:
    #     insert_vac_data(item, 100)
