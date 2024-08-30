# Проект: Работа с БД PostgreSQL и API hh.ru
## Описание
Данный проект предназначен для сбора и анализа данных о работодателях и вакансиях 
с использованием API hh.ru (HeadHunter). Он позволяет пользователю получать 
информацию о компаниях и их вакансиях, сохранять эту информацию в базе данных 
PostgreSQL и выполнять различные запросы для анализа данных. 

Проект состоит из нескольких модулей, которые взаимодействуют друг с другом:
1. main.py: Основной файл для запуска проекта. Инициализирует сбор данных и выполняет запросы к базе данных.
2. db_util.py: Модуль для создания базы данных и таблиц.
3. db_manager.py: Класс для взаимодействия с базой данных и выполнения запросов.
4. api_hh.py: Модуль для взаимодействия с API hh.ru и вставки данных в базу.
5. .env_sample: Конфигурация подключения к базе данных.


## Установка
- Клонируйте репозиторий на свой компьютер:

```
https://github.com/MichaelGorbunov/CW_5_DataBase
```

- Установите необходимые зависимости:
1. Создайте и активируйте виртуальное окружение poetry (рекомендуется)
2. Установите зависимости из pyproject.toml
3. Настройте подключение к базе данных в файле .env_sample и переименуйте его в .env. 
Для корректного первичного подключения необходимо наличие базы postgres на сервере.
4. В файл записан список id  работодателей
```
POSTGRES_HOST=localhost
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432
POSTGRES_DB=hh_database
EMP_ID_LIST="6041,2227671,2748,3776,3529,78638,4233,5390761,2180,906557"
```

## Использование
Для запуска приложения используйте команду:

python main.py

## Результат:
Скрипт выполнит следующие шаги:

1. Создаст базу данных и таблицы для хранения данных о компаниях и вакансиях.
2. Соберет данные о 10 работодателях и их вакансиях(первые 100) с помощью API hh.ru.
3. Сохранит собранные данные в базу данных.
4. Выполнит несколько запросов к базе данных и выведет результаты.

## Структура проекта
```
main.py               # Основной скрипт для запуска проекта
db_util.py            # Модуль для создания БД и таблиц
db_manager.py         # Модуль для выполнения запросов к базе данных
api_hh.py             # Модуль для взаимодействия с API hh.ru и заполнения БД
.env_sample           # Файл примера для конфигурации подключения к базе данных
README.md             # Описание проекта
```

## Лицензия
Проект предназначен для изучения Python,SQL,PostgreSQL и может использоваться для любых целей,
не противоречащих законодательству РФ.
