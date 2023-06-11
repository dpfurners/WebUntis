import datetime
from dataclasses import dataclass
import dataclasses


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

    def __init__(self, name, classes, teacher, room, start, end, canceled=False, substitution=False, **kwargs):
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

    def __getitem__(self, item):
        return self.lessons[item]


@dataclass
class Free:
    date: datetime.date
    reason: str


@dataclass
class Week:
    days: list[Day | Free]

    def __len__(self):
        return len(self.days)

    def __iter__(self):
        return iter(self.days)

    def __getitem__(self, item):
        return self.days[item]

    def __setitem__(self, key, value):
        self.days[key] = value

    """def __eq__(self, other):
        return other in [day.date for day in self.days]

    def __contains__(self, item: datetime.date | datetime.datetime):
        """#Check if the day is in this week"""
    """
        if isinstance(item, datetime.datetime):
            item = item.date()
        return item in [day.date for day in self.days]"""


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
        if isinstance(day, datetime.datetime):
            day = day.date()
        week = day.isocalendar().week
        if week not in self.weeks:
            return week
        return self.weeks[week].days[day.isocalendar().weekday - 1]

    def get_days(self, *days: datetime.date | datetime.datetime) -> list[int | Day | Free]:
        return [self.get_day(day) for day in days]

    def get_between(
            self,
            start: datetime.date | datetime.datetime,
            end: datetime.date | datetime.datetime
    ) -> list[int | Week] | Week | Day | Free:
        if not start.tzinfo and isinstance(start, datetime.datetime):
            start = datetime.datetime.combine(start.date(), start.time(), tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))
        if not end.tzinfo and isinstance(end, datetime.datetime):
            end = datetime.datetime.combine(end.date(), end.time(), tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))

        start_week = start.isocalendar().week
        end_week = end.isocalendar().week
        weeks_between = range(start_week, end_week + 1) if start_week != end_week else [start_week]
        weeks: list[Week | int] = self.get_weeks(*weeks_between)
        if not_loaded := [week for week in weeks if isinstance(week, int)]:
            return not_loaded
        # Remove days before start
        start_date = start.date() if isinstance(start, datetime.datetime) else start
        start_week_days = weeks[0]
        if isinstance(start, datetime.datetime):
            start_week_days_new = Week([day for day in start_week_days.days if day.date >= start_date])
            if not isinstance(start_week_days.days[0], Free):
                start_week_days_new[0] = dataclasses.replace(start_week_days_new.days[0])
                start_week_days_new[0].lessons = [
                    lesson for lesson in start_week_days_new.days[0].lessons if lesson.end >= start
                ]
        else:
            start_week_days_new = Week([day for day in start_week_days.days if day.date >= start_date])

        weeks[0] = start_week_days_new

        # Remove days after end
        end_date = end.date() if isinstance(end, datetime.datetime) else end
        end_week_days = weeks[-1]
        if isinstance(end, datetime.datetime):
            end_week_days_new = Week([day for day in end_week_days.days if day.date <= end_date])
            if not isinstance(end_week_days.days[-1], Free):
                end_week_days_new[-1] = dataclasses.replace(end_week_days_new.days[-1])
                end_week_days_new[-1].lessons = [
                    lesson for lesson in end_week_days_new.days[-1].lessons if lesson.start <= end
                ]
        else:
            end_week_days_new = Week([day for day in end_week_days.days if day.date <= end_date])

        weeks[-1] = end_week_days_new

        # Only one week between start and end
        if len(weeks) == 1:
            weeks: Week = weeks[0]

        # Only one day between start and end
        if len(weeks) == 1:
            weeks: Day | Free = weeks[0]

        return weeks
