import json
import os
import re
from typing import Any, Dict, List, Optional, Union

from src.API_HH import HHVacancyAPI


class UserInteraction:
    @staticmethod
    def format_salary(salary: Optional[Dict[str, Union[int, float]]]) -> str:
        """Форматирование зарплаты для отображения."""
        if not salary:
            return "Не указана"
        salary_from = salary.get("from")
        salary_to = salary.get("to")

        if salary_from and salary_to:
            return f"от {salary_from} до {salary_to}"
        elif salary_from:
            return f"от {salary_from}"
        elif salary_to:
            return f"до {salary_to}"
        else:
            return "Не указана"

    @staticmethod
    def remove_highlight_tags(text: str) -> str:
        """Удаление тегов <highlighttext> из строки."""
        if text:
            return re.sub(r"<highlighttext>|</highlighttext>", "", text)
        return text

    @staticmethod
    def display_top_vacancies(vacancies: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
        """Вывод топ N вакансий по зарплате."""

        def get_salary_from(vacancy: Dict[str, Any]) -> Any:
            """Получение значения 'from' зарплаты или 0, если не указана."""
            return vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"].get("from") else 0

        # Отсортировать вакансии по зарплате
        sorted_vacancies = sorted(vacancies, key=get_salary_from, reverse=True)
        top_vacancies = sorted_vacancies[:top_n]

        for i, vacancy in enumerate(top_vacancies, 1):
            salary = UserInteraction.format_salary(vacancy["salary"])
            description = UserInteraction.remove_highlight_tags(vacancy["snippet"]["requirement"])
            print(f"Вакансия {i}:")
            print(f"  Название: {vacancy['name']}")
            print(f"  Зарплата: {salary}")
            print(f"  Ссылка: {vacancy['alternate_url']}")
            print(f"  Описание: {description}")
            print("-" * 40)

        return top_vacancies

    @staticmethod
    def search_vacancies_by_description(vacancies: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
        """Поиск вакансий по ключевому слову в описании."""
        filtered_vacancies = [
            vacancy
            for vacancy in vacancies
            if vacancy["snippet"]["requirement"] and keyword.lower() in vacancy["snippet"]["requirement"].lower()
        ]
        for i, vacancy in enumerate(filtered_vacancies, 1):
            salary = UserInteraction.format_salary(vacancy["salary"])
            description = UserInteraction.remove_highlight_tags(vacancy["snippet"]["requirement"])
            print(f"Вакансия {i}:")
            print(f"  Название: {vacancy['name']}")
            print(f"  Зарплата: {salary}")
            print(f"  Ссылка: {vacancy['alternate_url']}")
            print(f"  Описание: {description}")
            print("-" * 40)

        return filtered_vacancies

    @staticmethod
    def save_to_json_result(data: Any, filename: str) -> None:
        """Сохранение данных в JSON файл"""
        directory = "data"

        # Создаем директорию 'data', если ее нет
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def user_interaction(cls) -> None:
        """Функция для взаимодействия с пользователем через консоль."""
        hh_api = HHVacancyAPI()

        # Получение поискового запроса от пользователя
        keyword = input("Введите поисковый запрос для поиска вакансий: ")

        # Получение вакансий по запросу
        vacancies = hh_api.get_vacancies(keyword)

        if not vacancies:
            print("Вакансии не найдены.")
            return

        # Получение количества вакансий для отображения
        try:
            top_n = int(input("Введите количество топ вакансий для отображения: "))
        except ValueError:
            print("Некорректное число. Пожалуйста, введите целое число.")
            return

        # Показать топ N вакансий по зарплате
        top_vacancies = cls.display_top_vacancies(vacancies, top_n)

        # Поиск вакансий с ключевым словом в описании среди топ N вакансий
        description_keyword = input("Введите ключевое слово для поиска в описании вакансий: ")
        filtered_vacancies = cls.search_vacancies_by_description(top_vacancies, description_keyword)

        # Данные для сохранения в JSON
        data_to_save = {
            "search_keyword": keyword,
            "top_vacancies": top_vacancies,
            "description_keyword": description_keyword,
            "filtered_vacancies": filtered_vacancies,
        }

        # Сохранение данных в JSON файл
        cls.save_to_json_result(data_to_save, "vacancies_results.json")
