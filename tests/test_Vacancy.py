from src.Vacancy import Vacancy, extract_salary_amount


def test_extract_salary_amount():
    """Тестирование функции извлечения зарплаты."""
    assert extract_salary_amount("от 1000") == 1000
    assert extract_salary_amount("до 2000") == 2000
    assert extract_salary_amount("1000") == 0  # Без "от" или "до"
    assert extract_salary_amount("Зарплата не указана") == 0


def test_vacancy_comparisons():
    """Тестирование сравнения вакансий по зарплате."""
    vacancy1 = Vacancy(
        id="1",
        title="Junior Developer",
        link="http://example.com",
        salary="от 1000",
        description="Junior developer role",
    )
    vacancy2 = Vacancy(
        id="2",
        title="Senior Developer",
        link="http://example.com",
        salary="до 2000",
        description="Senior developer role",
    )
    vacancy3 = Vacancy(
        id="3",
        title="Unpaid Intern",
        link="http://example.com",
        salary="Зарплата не указана",
        description="Internship role",
    )

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 != vacancy2
    assert vacancy1 != vacancy3

    # Проверка равенства
    vacancy1_2 = Vacancy(
        id="1",
        title="Junior Developer",
        link="http://example.com",
        salary="от 1000",
        description="Junior developer role",
    )
    assert vacancy1 == vacancy1_2
