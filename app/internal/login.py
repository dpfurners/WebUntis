import datetime

from fastapi import APIRouter, Response

from app.dependencies import DriverDependency, DriverNoAccountDepencency


router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


@router.get("/login", summary="Login to the account")
async def account_login(driver: DriverNoAccountDepencency, username: str, password: str):
    driver.login(username, password)
    return {"message": f"Logged in as {username}"}


@router.get("/logout", summary="Logout of the account")
async def account_logout(driver: DriverDependency):
    return {"message": f"You are now logged out"}


@router.get("/setschool", summary="Set the school (Not Implemented)")
async def set_school(driver: DriverNoAccountDepencency):
    return {"message": "New School Set"}
