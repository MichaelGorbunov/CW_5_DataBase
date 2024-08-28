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




def get_vacancies_by_employer(employer_id: int, per_page: int = 20) -> list[dict[str, Any]]:
    """
    Функция для получения списка вакансий работодателя с hh.ru.
    :param employer_id: ID работодателя.
    :param per_page: Количество вакансий на одной странице (по умолчанию 20).
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

    return vacancies_data.get("items", [])

if __name__ == '__main__':
    # main()
    # get_employers_by_name('МТС',100)
    get_vacancies_by_employer(3529,100)