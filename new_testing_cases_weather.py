import requests
import pytest
from datetime import datetime


@pytest.fixture()
def pass_url():
    return "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"


def cal_api():
    url = "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"
    api_resp = requests.get(url)
    return api_resp


def test_api_status():
    resp = cal_api()
    assert resp.status_code == 200
    pass


def test_case_1_response_for_4_days_of_data():
    resp = cal_api()
    json_resp = resp.json()
    day = set()
    for key, val in json_resp.items():
        if key == 'list':
            for each in val:
                for k, v in each.items():
                    if k == 'dt_txt':
                        datetime_object = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                        day.add(datetime_object.day)
    assert len(list(day)) == 4
    pass


def test_case_2_response_forecast_in_hourly_interval():
    resp = cal_api()
    json_resp = resp.json()
    hour = set()
    hour_data = list()
    hour_lists = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 23]
    for key, val in json_resp.items():
        if key == 'list':
            for each in val:
                for k, v in each.items():
                    if k == 'dt_txt':
                        datetime_object = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                        hour.add(datetime_object.hour)
                        for i in hour_lists:
                            if i in list(hour):
                                hour_test = True
                            else:
                                hour_test = False
                            hour_data.append(hour_test)
    assert hour_data == True
    pass


def test_case_3_min_max_temp():
    resp = cal_api()
    json_resp = resp.json()
    for key, val in json_resp.items():
        if key == 'list':
            for each in val:
                for k, v in each.items():
                    if k == 'main':
                        temp = v['temp']
                        min_temp = v['temp_min']
                        max_temp = v['temp_max']
                        assert (temp >= min_temp) and (temp <= max_temp)
    pass


def test_case_4_id_500_light_rain():
    resp = cal_api()
    json_resp = resp.json()
    for key, val in json_resp.items():
        if key == 'list':
            for each in val:
                for k, v in each.items():
                    if k == 'weather':
                        for each in v:
                            if each['id'] == 500:
                                required_condition = 'light rain'
                                condition = each['description'].strip()
                                assert condition == required_condition
    pass


def test_case_5_id_800_clear_sky():
    resp = cal_api()
    json_resp = resp.json()
    day = set()
    for key, val in json_resp.items():
        if key == 'list':
            for each in val:
                for k, v in each.items():
                    if k == 'weather':
                        for each in v:
                            if each['id'] == 800:
                                required_condition = 'clear sky'
                                condition = each['description'].strip()
                                assert condition == required_condition
    pass
