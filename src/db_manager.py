from abc import ABC, abstractmethod
from typing import Any, List, Tuple
import os
import psycopg2
from dotenv import load_dotenv



class DBManagerABC(ABC):
    """Абстрактный базовый класс для менеджера базы данных"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> List[Tuple[Any, ...]]:
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Tuple[Any, ...]]:
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> List[Tuple[Any, ...]]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[Any, ...]]:
        pass






class DBManager(DBManagerABC):
    def __init__(self):
        load_dotenv()
        db_config = {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "dbname": os.getenv("POSTGRES_DB"),
        }

        self.connection = psycopg2.connect(**db_config)
        self.connection.autocommit = True
        if self.connection:
            print("база открыта")

    def __del__(self):
        if self.connection:
            self.connection.close()
            print("соединения закрыто")

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        """возвращает среднюю зарплату по вакансиям."""
        with self.connection.cursor() as cur:
            cur.execute("""
                            SELECT AVG(salary_from) FROM vacancies;
                        """)
            avg_salary = round(cur.fetchone()[0])
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self, keyword:str):
        with self.connection.cursor() as cur:
            search_pattern = f"%{keyword.lower()}%"
            cur.execute(f"""
                SELECT companies.company_name, vacancies.vacan_title,
                vacancies.salary_from,vacancies.vacancy_url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                WHERE LOWER(vacancies.vacan_title) LIKE '{search_pattern}' OR  
                LOWER(vacancies.vacan_req) LIKE '{search_pattern}' OR
                LOWER(vacancies.vacan_resp) LIKE '{search_pattern}'
                ;
            """)
            result = cur.fetchall()
        return result


if __name__ == "__main__":
    db_manager = DBManager()
    # vacancies = db_manager.get_vacancies_with_keyword('кран')
    # for item in vacancies:
    #     print("'ыаыва':", item)
    print(db_manager.get_avg_salary())