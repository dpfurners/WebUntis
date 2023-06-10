import datetime
from dataclasses import dataclass


@dataclass
class Break:
    start: datetime.datetime
    end: datetime.datetime
    duration: datetime.timedelta


@dataclass
class Lesson:
    name: str
    classes: str
    teacher: str
    room: str
    canceled: bool
    substitution: bool
    duration: datetime.timedelta
    breaks: list[Break]
    start: datetime.datetime
    end: datetime.datetime

    def __init__(self, name, classes, teacher, room, start, end, canceled=False, substitution=False):
        self.name = name
        self.classes = classes
        self.teacher = teacher
        self.room = room
        self.canceled = canceled
        self.substitution = substitution
        self.start = start
        self.end = end
        self.duration = end - start
        self.breaks = []

    def __repr__(self):
        return f"Lesson(name={self.name}, {self.start.strftime('%H:%M')}-{self.end.strftime('%H:%M')}, breaks={self.breaks})"


@dataclass
class Day:
    date: datetime.date
    lessons: list[Lesson]
    canceled: list[Lesson]


@dataclass
class Free:
    reason: str


@dataclass
class Week:
    days: list[Day | Free]

    def __iter__(self):
        return iter(self.days)

    def __getitem__(self, item):
        return self.days[item]

    def __contains__(self, item: datetime.date | datetime.datetime):
        """Check if the day is in this week"""
        if isinstance(item, datetime.datetime):
            item = item.date()
        return item in [day.date for day in self.days]


@dataclass
class Collection:
    weeks: dict[int, Week]

    def __iter__(self):
        return iter(self.weeks.values())

    def __getitem__(self, item):
        return self.weeks[item]

    def __setitem__(self, key, value):
        self.weeks[key] = value

    def __len__(self):
        return len(self.weeks)

    def __repr__(self):
        return f"Collection(weeks={list(self.weeks.values())})"

    def get_week(self, week: int | datetime.date | datetime.datetime) -> int | Week:
        if isinstance(week, str):
            week = int(week)
        if isinstance(week, datetime.datetime) or isinstance(week, datetime.date):
            week = week.isocalendar().week
        if week not in self.weeks:
            return week
        return self.weeks[week]

    def get_weeks(self, *weeks: int | datetime.date | datetime.date) -> list[int | Week]:
        return [self.get_week(week) for week in weeks]

    def get_day(self, day: datetime.date | datetime.datetime) -> int | Day | Free:
        week = day.isocalendar().week
        if week not in self:
            return week
        if day.date() not in self.weeks[week].days:
            return day.isocalendar().week
        return self.weeks[week].days[day.isocalendar().weekday - 1]

    def get_days(self, *days: datetime.date | datetime.datetime) -> list[int | Day | Free]:
        return [self.get_day(day) for day in days]

    def get_between(self, start: datetime.date | datetime.datetime, end: datetime.date | datetime.datetime) -> list[int | Week]:
        start_week = start.isocalendar().week
        end_week = end.isocalendar().week
        weeks_between = range(start_week + 1, end_week) if start_week != end_week else [start_week]
        weeks = self.get_weeks(*weeks_between)
        if not_loaded := [week for week in weeks if isinstance(week, int)]:
            return not_loaded
        return weeks
