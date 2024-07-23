# Курсовая работа
## Описание:
Приложение для анализа вакансий на HH.ru. Оно позволяет сравнивать вакансии между собой
выводить вакансии по выбранному пользователем критерию, например по названию или описанию,
так же выводить ТОП вакансий и всю краткую информацию о них: Зарплата, Описание, Ссылку.
## Установка:
1. Клонируйте репозиторий:
```
git@github.com:Kostiik8/HomeWorkProject.git
```
2. Установите зависимости:
```
pip install poetry
poetry install
poetry add requests
pip install pytest
pip install  pytest-cov
poetry add --group lint mypy
poetry add --group lint black
poetry add --group lint isort
poetry add --group lint flake8 
poetry add requests-mock

```
## Тестирование
С помощью линтеров mypy, black, flake8, isort можете проверить код на соответствие PEP8
Пример команды:
```
flake8 module_name
flake8 . (все модули)
```

## Test Coverage
При необходимости можете проверить с помощью команд:
```
poetry add --group dev pytest
pytest --cov 
pytest  
```

## Модули
```
API_HH.py - Получает данные с HH.ru через API 
Filtered_vacancy.py - Взаимодействия с вакансиями: Сортировка, удаление, добавление
user_interaction.py - Взаимодействия с пользователем: Поиск по выбранным критериям, вывод Топ вакансий
Vacancy.py - Работа с вакансиями: Сравнение и оформление
main.py - вызов всей программы 
```