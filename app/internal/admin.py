import datetime

from fastapi import APIRouter

from app.dependencies import DriverDependency


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)


@router.get("/load", summary="Load a week")
async def load_week(driver: DriverDependency, week: int | datetime.date):
    driver.load_week(week)
    return {"message": f"Week {week} loaded..."}


@router.get("/already", summary="Get the already loaded weeks")
async def already_loaded(driver: DriverDependency):
    return {"message": f"Weeks {list(driver.weeks.weeks.keys())} loaded..."}