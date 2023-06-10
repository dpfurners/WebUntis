import datetime

from fastapi import APIRouter
from app.dependencies import DateTimeParameter, DateParameter, DriverDependency, TimeParameter
from app.scrape import day_info
from app.scrape.data import Lesson, Day

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
async def get_day_date(driver: DriverDependency, date: DateParameter) -> Day:
    return driver.weeks[date.isocalendar().week][date.isocalendar().weekday-1]


@router.get("/time", description="Returns the day with the lessons at the given time")
async def get_day_time(driver: DriverDependency, time: TimeParameter) -> list[Lesson]:
    day = driver.weeks[time.isocalendar().week][time.isocalendar().weekday-1]
    day_else = []
    for lesson in day.lessons:
        if lesson.end >= time:
            day_else.append(lesson)
    return day_else

