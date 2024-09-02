import os
import time

import psycopg2
from dotenv import load_dotenv

from src.api_hh import get_employers_info, get_vacancies_by_employer
from src.db_manager import DBManager
from src.db_util import (check_db, create_db, create_tables, insert_emp_data,
                         insert_vac_data)

start_time = time.time()

load_dotenv()


def main():
    db_create: bool
    db_create = check_db()
    if db_create is False:
        print(f"База {os.getenv("POSTGRES_DB")} не существует")
        create_db()
        print(f"База {os.getenv("POSTGRES_DB")} создана")
        create_tables()
        print(" таблицы созданы")
        print()
    else:
        print(f"База {os.getenv("POSTGRES_DB")} существует")
        create_tables()

    list_empl_str = os.getenv("EMP_ID_LIST").split(",")
    for item in list_empl_str:
        insert_emp_data(int(item))  # вставка данных о работодателях
        insert_vac_data(item, 100)  # вставка данных о вакансиях
        # get_employers_info(int(item))
        # get_vacancies_by_employer(int(item))

    print("Данные из api.hh.ru загружены ")
    db_manager = DBManager()

    print("Вывод списка работодателей и количества вакансий в базе ")
    print("--- %s seconds ---" % (time.time() - start_time))
    m = input("Нажмите Enter для продолжения")
    result = db_manager.get_companies_and_vacancies_count()
    for item in result:
        print(*item, sep=" ** ")

    # print("Все вакансии:")
    # m = input("Нажмите Enter для продолжения")
    # result = db_manager.get_all_vacancies() #все вакансии
    # for item in result:
    #     print(*item, sep=" ** ")
    #
    # print("Вычисление средней зарплаты:")
    # m = input("Нажмите Enter для продолжения")
    # result = db_manager.get_avg_salary()#Средняя зарплата
    # print(f"Средняя зарплата: {result}")
    #
    # print("Список вакансий c зарплатой выше средней:")
    # m = input("Нажмите Enter для продолжения")
    # result = db_manager.get_vacancies_with_higher_salary()
    # for item in result:
    #     print(*item, sep=" ** ")
    #
    # print("Поиск вакансий по ключевому слову")
    # keyword=input("Введите ключевое слово : ")
    # result = db_manager.get_vacancies_with_keyword(keyword)
    #
    # for item in result:
    #     print(*item, sep=" ** ")


if __name__ == "__main__":
    main()

    # print(db_config1)
    # list_empl:list[int] = []
    # env_list = os.getenv("EMP_ID_LIST")
    # list_empl_str=env_list.split(',')
    # for item in list_empl_str:
    #     list_empl.append(int(item))
    #
    # print(list_empl)
    # db_config1['dbname'] = "postgres"
    # print(db_config1)
