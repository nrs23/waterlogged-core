import requests

url = "https://api.open-meteo.com/v1/forecast"
payload = {"latitude": 50,
           "longitude": 0,
           "daily": ["precipitation_sum", "et0_fao_evapotranspiration"],
           "timezone": "auto",
           "past_days": 7}


def test_get_balance_data_check_status_code_equals_200():
    response = requests.get(url, params=payload)
    assert response.status_code == 200


def test_get_balance_data_check_content_type_equals_json():
    response = requests.get(url, params=payload)
    assert (response.headers["Content-Type"]
            ==
            "application/json; charset=utf-8")


def test_get_balance_data_check_daily_in_keys():
    response = requests.get(url, params=payload)
    response_json = response.json()
    assert "daily" in response_json


def test_get_balance_data_check_precipitation_in_daily():
    response = requests.get(url, params=payload)
    response_json = response.json()
    assert "precipitation_sum" in response_json["daily"]


def test_get_balance_data_check_et0_in_daily():
    response = requests.get(url, params=payload)
    response_json = response.json()
    assert "et0_fao_evapotranspiration" in response_json["daily"]


def test_get_balance_data_check_number_of_days():
    response = requests.get(url, params=payload)
    response_json = response.json()
    assert len(response_json["daily"]["precipitation_sum"]) == 14
