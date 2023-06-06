import datetime

from fastapi import APIRouter, Depends, Request
from app.dependencies import DateTimeParameter, DateParameter, DriverDependency, TimeParameter
from app.scrape import day_info

router = APIRouter(
    prefix="/day",
    tags=["day"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_day_info(driver: DriverDependency, day: DateTimeParameter) -> dict:
    if isinstance(day, datetime.datetime):
        return day_info(driver.weeks[day.isocalendar().week][day.isocalendar().weekday - 1], day)
    return day_info(driver.weeks[day.isocalendar().week][day.isocalendar().weekday - 1])


@router.get("/date")
async def get_day_date(driver: DriverDependency, date: DateParameter) -> dict:
    if date is None:
        day = datetime.date.today()
    return driver.weeks[date.isocalendar().week][date.isocalendar().weekday-1]


@router.get("/time")
async def get_day_time(driver: DriverDependency, time: TimeParameter) -> dict:
    if time is None:
        time = datetime.datetime.now()
    return driver.weeks[time.isocalendar().week][time.isocalendar().weekday-1]

