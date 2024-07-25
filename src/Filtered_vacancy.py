import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.API_HH import HHVacancyAPI
from src.Vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с файлами хранения вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Any) -> None:
        """Добавление вакансии в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """Получение данных из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy_by_title(self, title: str) -> None:
        """Удаление информации о вакансии из файла по названию."""
        pass


class JSONVacancyStorage(VacancyStorage):
    """Класс для работы с JSON-файлом для хранения вакансий."""

    def __init__(self, filename: str):
        # Обновляем путь к файлу, чтобы сохранять его в директорию 'data'
        self.filename = os.path.join("../data", filename)
        if not os.path.exists("../data"):
            os.makedirs("../data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)
        else:
            # Проверяем, что файл не пустой и имеет правильный формат
            try:
                with open(self.filename, "r") as file:
                    json.load(file)
            except json.JSONDecodeError:
                with open(self.filename, "w") as file:
                    json.dump([], file)

    def add_vacancy(self, vacancy: Any) -> None:
        """Добавление вакансии в JSON-файл."""
        try:
            with open(self.filename, "r") as file:
                vacancies = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            vacancies = []

        vacancies.append(vacancy.__dict__)

        try:
            with open(self.filename, "w") as file:
                json.dump(vacancies, file, indent=4)
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")

    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """Получение данных из JSON-файла по указанным критериям."""
        try:
            with open(self.filename, "r") as file:
                vacancies = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            if "title" in criteria and vacancy.get("title") != criteria["title"]:
                match = False
            if "min_salary" in criteria:
                min_salary = criteria["min_salary"]
                vacancy_salary_from = vacancy.get("salary", {}).get("from", 0)
                if vacancy_salary_from is None or vacancy_salary_from < min_salary:
                    match = False
            if "max_salary" in criteria:
                max_salary = criteria["max_salary"]
                vacancy_salary_to = vacancy.get("salary", {}).get("to", float("inf"))
                if vacancy_salary_to is None or vacancy_salary_to > max_salary:
                    match = False
            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy_by_title(self, title: str) -> None:
        """Удаление вакансии из JSON-файла по названию."""
        try:
            with open(self.filename, "r") as file:
                vacancies = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return

        # Фильтрация вакансий, исключая те, у которых название совпадает с указанным
        vacancies_to_keep = [vacancy for vacancy in vacancies if vacancy.get("title") != title]

        try:
            with open(self.filename, "w") as file:
                json.dump(vacancies_to_keep, file, indent=4)
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")


def save_to_json_file(data, filename: Any) -> None:
    """Сохранение данных в JSON-файл."""
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")


hh_api = HHVacancyAPI()
vacancies_data = hh_api.get_vacancies("Python Developer")

# Создаем и сохраняем вакансии
json_storage = JSONVacancyStorage("vacancies.json")

for vacancy_data in vacancies_data:
    vacancy = Vacancy(
        id=vacancy_data["id"],
        title=vacancy_data["name"],
        link=vacancy_data["alternate_url"],
        salary=vacancy_data["salary"],
        description=vacancy_data["snippet"]["requirement"],
    )
    json_storage.add_vacancy(vacancy)

# Получаем вакансии по критерию
filtered_vacancies = json_storage.get_vacancies(title="Python Developer")
save_to_json_file(filtered_vacancies, "filtered_vacancies.json")

# Удаление вакансии по названию
json_storage.delete_vacancy_by_title("Middle React developer [CMDB]")

# Проверка, что вакансия удалена
remaining_vacancies = json_storage.get_vacancies()
save_to_json_file(remaining_vacancies, "remaining_vacancies.json")
