import os
import time

import psycopg2
from dotenv import load_dotenv
from src.db_util import create_db,create_tables
from src.api_hh import insert_vac_data,insert_emp_data
from src.db_manager import DBManager
start_time = time.time()

load_dotenv()

db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB")
}


def check_db() -> bool:
    """функция проверяет наличие базы данных """
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
            return False
        else:
            return True
        conn.close()





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


    list_empl_str=os.getenv("EMP_ID_LIST").split(',')
    for item in list_empl_str:
        insert_emp_data(int(item))#вставка данных о работодателях
        insert_vac_data(item, 100)#вставка данных о вакансиях

    print("Данные из api.hh.ru загружены ")
    db_manager=DBManager()

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
