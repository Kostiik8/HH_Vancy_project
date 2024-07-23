import pytest

from src.Filtered_vacancy import JSONVacancyStorage
from src.Vacancy import Vacancy


@pytest.fixture
def storage(tmpdir):
    """Фикстура для создания временного хранилища вакансий."""
    filename = tmpdir.join("test_vacancies.json")
    storage = JSONVacancyStorage(str(filename))

    yield storage


def test_add_vacancy(storage):
    """Тестирование добавления вакансии в хранилище."""
    vacancy = Vacancy(
        id="1",
        title="Software Engineer",
        link="http://example.com/vacancy1",
        salary={"from": 100000, "to": 120000},
        description="Описание вакансии",
    )
    storage.add_vacancy(vacancy)

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Software Engineer"


def test_get_vacancies_by_criteria(storage):
    """Тестирование получения вакансий по критериям."""
    vacancy1 = Vacancy(
        id="1",
        title="Software Engineer",
        link="http://example.com/vacancy1",
        salary={"from": 100000, "to": 120000},
        description="Описание вакансии",
    )
    vacancy2 = Vacancy(
        id="2",
        title="Data Scientist",
        link="http://example.com/vacancy2",
        salary={"from": 90000, "to": 110000},
        description="Описание вакансии",
    )
    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    vacancies = storage.get_vacancies(title="Data Scientist")
    assert vacancies[0]["title"] == "Data Scientist"


def test_delete_vacancy(storage):
    """Тестирование удаления вакансии по названию."""
    vacancy = Vacancy(
        id="1",
        title="Software Engineer",
        link="http://example.com/vacancy1",
        salary={"from": 100000, "to": 120000},
        description="Описание вакансии",
    )
    storage.add_vacancy(vacancy)

    storage.delete_vacancy_by_title("Software Engineer")
