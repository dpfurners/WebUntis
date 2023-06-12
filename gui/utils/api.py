import datetime

import requests


URL = "http://127.0.0.1:8000"


def request(url: str, **params) -> dict:
    req = requests.get(url, params=params)
    if req.status_code != 200:
        raise ValueError(req.json()["message"])
    return req.json()


def load_day(date: datetime.datetime | datetime.date) -> dict:
    if isinstance(date, datetime.datetime):
        return request(URL + "/day/time/", time=date)
    if isinstance(date, datetime.date):
        return request(URL + "/day/date/", day=date)


def load_day_info(date: datetime.datetime | datetime.date) -> dict:
    return request(URL + "/day/", dt=date)


if __name__ == '__main__':
    print(load_day(datetime.datetime(2023, 6, 12, 10, 20)))

