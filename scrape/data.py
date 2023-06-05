import datetime
from dataclasses import dataclass


@dataclass
class Lesson:
    name: str
    classes: str
    teacher: str
    room: str
    canceled: bool
    substitution: bool
    start: datetime.datetime
    end: datetime.datetime


@dataclass
class Day:
    date: datetime.date
    lessons: list[Lesson]


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
