import datetime

from fastapi import APIRouter, Response

from app.dependencies import DriverDependency, DriverNoAccountDepencency


router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


@router.get("/login")
async def load_week(driver: DriverNoAccountDepencency, username: str, password: str):
    driver.login(username, password)
    return {"message": f"Logged in as {username}"}


@router.get("/logout")
async def already_loaded(driver: DriverDependency):
    return {"message": f"You are now logged out"}


@router.get("/setschool")
async def set_school(driver: DriverNoAccountDepencency):
    return {"message": "New School Set"}
