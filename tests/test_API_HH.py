import pytest
import requests_mock
from src.API_HH import HHVacancyAPI


@pytest.fixture
def hh_api():
    return HHVacancyAPI()


def test_get_vacancies_success(hh_api):
    keyword = "Python Developer"
    url = "https://api.hh.ru/vacancies"

    mock_response = {
        "items": [
            {
                "id": "1",
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {"requirement": "Experience with Python"},
            },
            {
                "id": "2",
                "name": "Senior Python Developer",
                "alternate_url": "https://hh.ru/vacancy/2",
                "salary": {"from": 200000, "to": 250000},
                "snippet": {"requirement": "5 years of experience with Python"},
            },
        ]
    }

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_response)
        vacancies = hh_api.get_vacancies(keyword)

    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[0]["salary"]["from"] == 100000
    assert vacancies[1]["name"] == "Senior Python Developer"
    assert vacancies[1]["salary"]["from"] == 200000


def test_get_vacancies_invalid_params(hh_api):
    hh_api.params["page"] = "invalid"
    keyword = "Python Developer"

    with pytest.raises(ValueError):
        hh_api.get_vacancies(keyword)
