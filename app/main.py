import datetime
import uvicorn

from fastapi import FastAPI

from scrape import WebuntisDriver, day_info

from routers import day, week, year
from internal import admin


async def lifespan(application: FastAPI):
    driver = WebuntisDriver()
    driver.login()
    driver.load_week(datetime.date.today())
    application.
    application.state.driver = driver
    yield
    application.state.driver.close()


app = FastAPI(lifespan=lifespan)

app.include_router(day.router)
app.include_router(admin.router)
# app.include_router(week.router)
# app.include_router(year.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host="localhost")
