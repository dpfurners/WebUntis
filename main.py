import datetime
import uvicorn

from fastapi import FastAPI

from scrape import WebuntisDriver


async def lifespan(application: FastAPI):
    global driver
    driver = WebuntisDriver()
    driver.login()
    driver.load_week(datetime.date.today())
    yield
    driver.close()

driver: WebuntisDriver = None

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/load/{week}")
async def load_week(week: int | datetime.date):
    global driver
    driver.load_week(week)
    return {"message": f"Week {week} loaded..."}


@app.get("/already")
async def already_loaded():
    global driver
    return {"message": f"Weeks {list(driver.weeks.keys())} loaded..."}


@app.get("/info/day")
async def get_day_info(day: datetime.date):
    global driver
    if day.isocalendar().week not in driver.weeks:
        driver.load_week(day)
    return driver.weeks[day.isocalendar().week][day.isocalendar().weekday-1]

@app.get("/day/{day}")
async def get_day(day: datetime.date | None):
    print(day)
    global driver
    if day is None:
        day = datetime.date.today()
    if day.isocalendar().week not in driver.weeks:
        driver.load_week(day)
    return driver.weeks[day.isocalendar().week][day.isocalendar().weekday-1]

if __name__ == '__main__':
    uvicorn.run(app, host="localhost")
