import datetime
from pathlib import Path

import uvicorn

from fastapi import FastAPI

from scrape import WebuntisDriver

from routers import day
from internal import admin
from logs import CustomizeLogger

config_path = Path(__file__).parent / "logs" / "config.json"

logger = CustomizeLogger.make_logger(config_path)


async def lifespan(application: FastAPI):
    global logger
    application.logger = logger
    driver = WebuntisDriver(True)
    driver.login()
    driver.load_week(datetime.date.today())
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
