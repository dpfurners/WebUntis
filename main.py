import datetime
import uvicorn

from fastapi import FastAPI

from scrape import WebuntisDriver


async def lifespan(application: FastAPI):
    driver = WebuntisDriver()
    driver.login()
    week = driver.load_week(datetime.date.today())
    print(week)
    yield
    driver.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    uvicorn.run(app, host="localhost")
