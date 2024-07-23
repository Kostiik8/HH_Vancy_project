import pytest

from src.user_interaction import UserInteraction


@pytest.fixture
def sample_vacancies():
    """Фикстура для предоставления примера вакансий."""
    return [
        {
            "name": "Вакансия 1",
            "salary": {"from": 150000, "to": 200000},
            "alternate_url": "http://example.com/vacancy1",
            "snippet": {"requirement": "Опыт работы в Python <highlighttext>желателен</highlighttext>"},
        },
        {
            "name": "Вакансия 2",
            "salary": {"from": 120000},
            "alternate_url": "http://example.com/vacancy2",
            "snippet": {"requirement": "Знание Django <highlighttext>обязательно</highlighttext>"},
        },
        {
            "name": "Вакансия 3",
            "salary": {"to": 100000},
            "alternate_url": "http://example.com/vacancy3",
            "snippet": {"requirement": "Знание Java"},
        },
    ]


def test_format_salary():
    assert UserInteraction.format_salary({"from": 100000, "to": 150000}) == "от 100000 до 150000"
    assert UserInteraction.format_salary({"from": 100000}) == "от 100000"
    assert UserInteraction.format_salary({"to": 150000}) == "до 150000"
    assert UserInteraction.format_salary({}) == "Не указана"
    assert UserInteraction.format_salary(None) == "Не указана"


def test_remove_highlight_tags():
    assert UserInteraction.remove_highlight_tags("Текст <highlighttext>с тегами</highlighttext>") == "Текст с тегами"
    assert UserInteraction.remove_highlight_tags("Без тегов") == "Без тегов"
    assert UserInteraction.remove_highlight_tags("") == ""


def test_display_top_vacancies(capfd, sample_vacancies):
    UserInteraction.display_top_vacancies(sample_vacancies, 2)
    captured = capfd.readouterr()
    assert "Вакансия 1:" in captured.out
    assert "Вакансия 2:" in captured.out
    assert "Вакансия 3:" not in captured.out


def test_search_vacancies_by_description(capfd, sample_vacancies):
    UserInteraction.search_vacancies_by_description(sample_vacancies, "Python")
    captured = capfd.readouterr()
    assert "Вакансия 1:" in captured.out
    assert "Вакансия 2:" not in captured.out
    assert "Вакансия 3:" not in captured.out
