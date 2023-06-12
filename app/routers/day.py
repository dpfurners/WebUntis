import datetime

from fastapi import APIRouter
from app.dependencies import DateTimeParameter, DateParameter, DriverDependency, TimeParameter
from app.scrape import day_info
from app.scrape.data import Day, Free
from app.scrape.info.day import DayInfo

router = APIRouter(
    prefix="/day",
    tags=["day"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Get information about the current/specified day")
async def get_day_info(driver: DriverDependency, day: DateTimeParameter) -> DayInfo | Free:
    if day.isocalendar().weekday in (6, 7):
        return Free(day.date() if isinstance(day, datetime.datetime) else day, "Weekend")
    if isinstance(day, datetime.datetime):
        return day_info(driver.weeks.get_between(
            day, datetime.datetime.combine(day.date(), datetime.time(23, 59, 59), day.tzinfo)), day)
    return day_info(driver.weeks.get_day(day))


@router.get("/date", summary="Get the lessons of a day")
async def get_day_date(driver: DriverDependency, date: DateParameter) -> Day | dict | Free:
    if date.isocalendar().weekday in (6, 7):
        return Free(date, "Weekend")
    return driver.weeks.get_day(date)


@router.get("/time", summary="Returns the day with the lessons from the given time")
async def get_day_time(driver: DriverDependency, time: TimeParameter) -> Day | Free:
    if time.isocalendar().weekday in (6, 7):
        return Free(time.date(), "Weekend")
    return driver.weeks.get_between(time, datetime.datetime.combine(time.date(), datetime.time(23, 59, 59), time.tzinfo))
