import datetime
from dataclasses import dataclass, field

from app.scrape.data import Day
from app.scrape.info.model import InfoCollection, DateInfo


def day_lessons_overview(day: Day):
    start_end = [(les.start, les.end) for les in day.lessons]
    dups = []
    for start, end in start_end:
        if dup := [i for i, x in enumerate(start_end) if x == (start, end)]:
            if dup not in dups:
                dups.append(dup)
    lessons = []
    for les in dups:
        if len(les) == 1:
            lessons.append(day.lessons[les[0]].name)
        else:
            if day.lessons[les[0]].name == day.lessons[les[1]].name:
                lessons.append(day.lessons[les[0]].name)
            else:
                lessons.append(f"{day.lessons[les[0]].name} | {day.lessons[les[1]].name}")
    return lessons


@dataclass
class DayInfo(InfoCollection):
    date_info: DateInfo = field(default_factory=DateInfo)
    lesson_overview: list[str] = field(default_factory=list[str])

    def __init__(self, day: Day, dt: datetime.datetime = None):
        self.date_info = DateInfo(day, dt)
        self.lesson_overview = day_lessons_overview(day)
        super().__init__(day)


def day_info(day: Day, dt: datetime.datetime = None) -> DayInfo:
    return DayInfo(day, dt)
