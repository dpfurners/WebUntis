from bs4 import BeautifulSoup

import datetime
import urllib.parse

from .data import Week, Day, Lesson, Free


CANCELLED = ["background-color: rgba(177, 179, 180, 0.3)", "background-color: rgba(177, 179, 180, 0.7)"]
SUBSTITUTIONED = ["background-color: rgba(167, 129, 181, 0.3)", "background-color: rgba(167, 129, 181, 0.7)"]


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


def resolve_free_days(soup: BeautifulSoup):
    days = soup.find_all("div", {"class": "timetableGridColumn"})[5:]
    free = []
    for day in days:
        if style := day.get("style"):
            style = style.split("; ")
            if "background-color: rgba(162, 216, 244, 0.75);" in style:
                free.append(Free(day.text))
                continue
        free.append(None)
    return free


def resolve_longer_hours(week: Week):
    """for day in [d for d in week if isinstance(d, Day)]:
        for i in range(len(day.lessons) - 1):
            try:
                if day.lessons[i].name == day.lessons[i + 1].name \
                        and day.lessons[i].teacher == day.lessons[i + 1].teacher \
                        and day.lessons[i].room == day.lessons[i + 1].room:
                    day.lessons[i].end = day.lessons[i + 1].end
                    day.lessons[i].duration = day.lessons[i].end - day.lessons[i].start
                    if day.lessons[i].end != day.lessons[i + 1].start:
                        day.lessons[i].breaks.append(
                            (day.lessons[i].end,
                             day.lessons[i + 1].start,
                             day.lessons[i + 1].start - day.lessons[i].end))
                    day.lessons[i].breaks.extend(day.lessons[i + 1].breaks)
                    day.lessons.pop(i + 1)
            except IndexError:
                pass"""
    return week


def scrape_week(req_day: datetime.date, page_source=None) -> Week:
    if page_source is None:
        page_source = read_page_source()
    soup = BeautifulSoup(page_source, "html.parser")
    hours = soup.find_all("a", {"target": "_blank"}, href=True)
    week_hours: list[Lesson] = []
    week: Week = Week([])
    for hour in hours:
        start, end = resolve_start_end(hour["href"])
        info = hour.find("table", {"class": "centerTable"})
        try:
            classes, teacher, name, room = [i.text for i in info.find_all("td")]
        except ValueError:
            classes, teacher, name = [i.text for i in info.find_all("td")]
            room = "I251"
        canceled = False
        substitution = False
        if style := hour.find_next("div").get("style"):
            styles = style.split("; ")
            if CANCELLED[0] in styles or CANCELLED[1] in styles:
                canceled = True
            if SUBSTITUTIONED[0] in styles or SUBSTITUTIONED[1] in styles:
                substitution = True

        week_hours.append(Lesson(name, classes, teacher, room, start, end, canceled, substitution))
    week_hours.sort(key=lambda x: x.start)
    print(len([hour for hour in week_hours]))

    free = resolve_free_days(soup)
    first_day = req_day - datetime.timedelta(days=req_day.isoweekday() - 1)

    for i in range(5):
        if free[i]:
            week.days.append(free[i])
            continue
        d = Day(
            first_day + datetime.timedelta(days=i),
            lessons=[day for day in week_hours
                     if day.start.date() == first_day + datetime.timedelta(days=i) and not day.canceled],
            canceled=[day for day in week_hours
                      if day.start.date() == first_day + datetime.timedelta(days=i) and day.canceled]
        )
        week.days.append(d)

    week = resolve_longer_hours(week)
    return week


if __name__ == '__main__':
    scrape_week()
