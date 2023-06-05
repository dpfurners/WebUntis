from bs4 import BeautifulSoup

import datetime
import urllib.parse

from .data import Week, Day, Lesson


def write_page_source(source):
    with open("test.html", "w", encoding="utf-8") as f:
        soup = BeautifulSoup(source, "html.parser")
        f.write(soup.prettify())


def read_page_source():
    with open("test.html", "r", encoding="utf-8") as f:
        return f.read()


def resolve_start_end(href: str) -> tuple[datetime.datetime, datetime.datetime]:
    dates = href.split("/")[-3:-1]
    start = datetime.datetime.strptime(urllib.parse.unquote(dates[0]), "%Y-%m-%dT%H:%M:%S%z")
    end = datetime.datetime.strptime(urllib.parse.unquote(dates[1]), "%Y-%m-%dT%H:%M:%S%z")
    return start, end


def scrape_week(page_source=None) -> Week:
    if page_source is None:
        page_source = read_page_source()
    soup = BeautifulSoup(page_source, "html.parser")
    hours = soup.find_all("a", {"target": "_blank"}, href=True)
    hours_styles = soup.find_all("a", {"target": "_blank"}, style=False)
    week_hours: list[Lesson] = []
    week: Week = Week([])
    for hour, style in zip(hours, hours_styles):
        start, end = resolve_start_end(hour["href"])
        info = hour.find("table", {"class": "centerTable"})
        classes, teacher, name, room = info.find_all("td")
        canceled = False
        substitution = False
        if style := style.find_next("div").get("style"):
            styles = style.split("; ")
            print(styles)
            if "background-color: rgba(177, 179, 180, 0.3)" in styles:
                canceled = True
            if "background-color: rgba(167, 129, 181, 0.7)" in styles:
                substitution = True

        week_hours.append(Lesson(name.text, classes.text, teacher.text, room.text, canceled, substitution,  start, end))
    week_hours.sort(key=lambda x: x.start)

    today = datetime.date.today()
    first_day = today - datetime.timedelta(days=today.isoweekday() - 1)
    for i in range(5):
        d = Day(
            first_day + datetime.timedelta(days=i),
            lessons=[day for day in week_hours if day.start.date() == first_day + datetime.timedelta(days=i)]
        )
        week.days.append(d)
    return week


if __name__ == '__main__':
    scrape_week()
