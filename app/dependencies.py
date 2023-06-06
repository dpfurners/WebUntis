import datetime

from typing import Annotated
from fastapi import Depends, Request

from app.scrape import WebuntisDriver


async def get_driver(request: Request):
    return request.app.state.driver


async def load_week(week: int | datetime.date, driver: WebuntisDriver):
    driver.load_week(week)


async def datetime_parameter(request: Request, dt: datetime.date | datetime.datetime, time_specific: bool = False):
    driver: WebuntisDriver = request.app.state.driver
    if isinstance(dt, datetime.datetime) and not time_specific:
        dt = dt.date()
    await load_week(dt, driver)
    return datetime


async def date_parameter(request: Request, day: datetime.date):
    driver: WebuntisDriver = request.app.state.driver
    await load_week(day, driver)
    return day


async def time_parameter(request: Request, time: datetime.datetime):
    driver: WebuntisDriver = request.app.state.driver
    await load_week(time, driver)
    return time


DateTimeParameter = Annotated[datetime.date, datetime.datetime, Depends(datetime_parameter)]

DateParameter = Annotated[datetime.date, Depends(date_parameter)]

TimeParameter = Annotated[datetime.datetime, Depends(time_parameter)]

DriverDependency = Annotated[WebuntisDriver, Depends(get_driver)]


