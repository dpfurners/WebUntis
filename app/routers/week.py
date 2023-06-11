import datetime

from fastapi import APIRouter
from app.dependencies import DateTimeParameter, DateParameter, DriverDependency, TimeParameter
from app.scrape import week_info
from app.scrape.data import Day, Free
from app.scrape.info.week import WeekInfo

router = APIRouter(
    prefix="/week",
    tags=["week"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_week_info(driver: DriverDependency, week: DateParameter) -> WeekInfo | Free:
    return week_info(driver.weeks.get_week(week))


@router.get("/date")
async def get_day_date(driver: DriverDependency, date: DateParameter) -> Day | dict | Free:
    return driver.weeks.get_weeks(date)

