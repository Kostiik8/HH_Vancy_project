from src.API_HH import HHVacancyAPI


def extract_salary_amount(salary):
    """Извлечение числового значения из строки зарплаты."""
    if "от" in salary:
        return int(salary.split(" ")[1])
    elif "до" in salary:
        return int(salary.split(" ")[1])
    return 0


class Vacancy:
    """Класс для работы с вакансиями."""

    def __init__(self, id, title, link, salary, description):
        self.id = id
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

    def __lt__(self, other):
        """Сравнение вакансий по зарплате."""
        if self.salary == "Зарплата не указана":
            return False
        elif other.salary == "Зарплата не указана":
            return True
        else:
            return extract_salary_amount(self.salary) < extract_salary_amount(other.salary)

    def __gt__(self, other):
        """Сравнение вакансий по зарплате."""
        if self.salary == "Зарплата не указана":
            return True
        elif other.salary == "Зарплата не указана":
            return False
        else:
            return extract_salary_amount(self.salary) > extract_salary_amount(other.salary)

    def __eq__(self, other):
        """Сравнение вакансий по зарплате."""
        if self.salary == "Зарплата не указана" or other.salary == "Зарплата не указана":
            return False
        else:
            return extract_salary_amount(self.salary) == extract_salary_amount(other.salary)


hh_api = HHVacancyAPI()
vacancies = hh_api.get_vacancies("keyword")

for vacancy_data in vacancies:
    vacancy = Vacancy(
        id=vacancy_data["id"],
        title=vacancy_data["name"],
        link=vacancy_data["alternate_url"],
        salary=vacancy_data["salary"],
        description=vacancy_data["snippet"]["requirement"],
    )
