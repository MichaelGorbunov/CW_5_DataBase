import requests
from typing import Any


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
    """

    """
    url = f"https://api.hh.ru/employers/{employer_id}"
    employer=[]

    response = requests.get(url)
    response.raise_for_status()
    employers_data = response.json()
    # print(employers_data.get("description"))
    # print(employers_data.get("name"))
    # print(employers_data.get("site_url"))
    employer.append(
            {
                "company_id":employer_id,
                "company_name":employers_data.get("name"),
                "company_desc":employers_data.get("description"),
                "company_url":employers_data.get("site_url")
            })
    return employer




def get_vacancies_by_employer(employer_id: int, per_page: int = 20) -> list[dict[str, Any]]:
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
                "id": int(vacans.get("id")),
                "company_id": employer_id,
                "name": vacans.get("name"),
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
                "url": vacans.get("url"),
                "requirement": (
                    vacans.get("snippet").get("requirement")
                    if vacans.get("snippet").get("requirement") is not None
                    else "Не указано"
                ),
                "responsibility": (
                    vacans.get("snippet").get("responsibility")
                    if vacans.get("snippet").get("responsibility") is not None
                    else "Не указано"
                ),
            }
        )
    return vacancies


if __name__ == '__main__':
    # main()
    # get_employers_by_name('МТС',100)
    # print(get_vacancies_by_employer(3529, 100))
    # print(get_employers_info(6040))

    # for item in [6041,2227671,2748,3776,3529,78638,4233,5390761,2180,906557]:
    #     get_employers_info(item)
    for item in [6041, 2227671, 2748, 3776, 3529, 78638, 4233, 5390761, 2180, 906557]:
        print(get_employers_info(item))
        vacan=get_vacancies_by_employer(item,15)
        for item in vacan:
            print(item)