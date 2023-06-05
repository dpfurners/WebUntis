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
    breaks: list[tuple[datetime.datetime, datetime.datetime, datetime.timedelta]]
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
