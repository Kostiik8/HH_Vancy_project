from abc import ABC, abstractmethod

import requests


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def get_vacancies(self, keyword):
        """Получение списка вакансий по ключевому слову."""
        pass


class HHVacancyAPI(VacancyAPI):
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 20}

    def get_vacancies(self, keyword):
        """Получение списка вакансий по ключевому слову."""
        self.params["text"] = keyword
        vacancies = []

        if not isinstance(self.params["page"], int) or not isinstance(self.params["per_page"], int):
            raise ValueError("Параметры 'page' и 'per_page' должны быть целыми числами")

        while self.params["page"] < 20:
            request_params = {k: (str(v) if v is not None else '') for k, v in self.params.items()}
            response = requests.get(self.url, headers=self.headers, params=request_params)
            if response.status_code == 200:
                vacancies.extend(response.json()["items"])
                self.params["page"] += 1
            else:
                break
        return vacancies
