import datetime
from dataclasses import dataclass, field

from app.scrape.data import Day, Week, Free


@dataclass
class ClassInfo:
    name: str = field(default_factory=str)
    teacher: list[str] = field(default_factory=list[str])
    room: list[str] = field(default_factory=list[str])
    times: int = field(default_factory=int)
    cancellations: int = field(default_factory=int)
    substitutions: int = field(default_factory=int)


@dataclass
class LessonInfo:
    overall_lessons: int = field(default=0)
    overall_hours: float = field(default=0.0)
    cancelled_lessons: int = field(default=0)
    cancelled_hours: float = field(default=0.0)
    substituted_lessons: int = field(default=0)
    substituted_hours: float = field(default=0.0)
    classes: list[ClassInfo] = field(default_factory=list[ClassInfo])

    def round_numbers(self):
        self.overall_hours = round(self.overall_hours, 2)
        self.cancelled_hours = round(self.cancelled_hours, 2)
        self.substituted_hours = round(self.substituted_hours, 2)


@dataclass
class FreeLessonInfo(LessonInfo):
    free_days: int = field(default=0)
    free_because: list[str] = field(default_factory=list[str])


@dataclass
class DateInfo:
    day: datetime.date
    time: datetime.datetime | str
    week: int
    weekday: str

    def __init__(self, day: Day, dt: datetime.datetime = None):
        self.day = day.date
        self.time = dt if dt else "all"
        self.week = day.date.isocalendar().week
        self.weekday = day.date.strftime("%A")


@dataclass
class InfoCollection:
    lesson_info: LessonInfo | FreeLessonInfo = field(default_factory=LessonInfo)

    def __init__(self, *data: Day | Week):
        self.lesson_info = self._lesson_info(*data)

    @staticmethod
    def _lesson_info(*data: Day | Week | Free) -> LessonInfo | FreeLessonInfo:
        days = []
        if isinstance(data[0], Week):
            for week in data:
                days += week.days
        else:
            days = list(data)

        try:
            for day in days:
                day.__getattribute__("lessons")
            lesson_info = LessonInfo()
        except AttributeError as e:
            lesson_info = FreeLessonInfo()

        for day in days:
            # print(type(day), isinstance(day, Free), day.__getattribute__("reason"))
            try:
                day.__getattribute__("reason")
                lesson_info.free_days += 1
                if day.reason not in lesson_info.free_because:
                    lesson_info.free_because.append(day.reason)
                    continue
            except AttributeError as e:
                pass
            lessons = day.lessons
            simultaneous_lessons = 0
            lesson_info.cancelled_lessons += len([les for les in lessons if les.canceled])
            lesson_info.cancelled_hours += sum([
                int(les.duration.total_seconds())/3600 for les in lessons if les.canceled
            ])
            lesson_info.substituted_hours = len([les for les in lessons if les.substitution])
            lesson_info.substituted_hours += sum([
                int(les.duration.total_seconds())/3600 for les in lessons if les.substitution
            ])
            for lesson in lessons:
                if simultaneous_les := [les for les in lessons if les.start == lesson.start and les.end == lesson.end]:
                    simultaneous_lessons += len(simultaneous_les) - 1
                if classes_info := [lesn for lesn in lesson_info.classes if lesn.name == lesson.name]:
                    classes_info[0].times += 1
                    classes_info[0].cancellations += 1 if lesson.canceled else 0
                    classes_info[0].substitutions += 1 if lesson.substitution else 0
                    if lesson.teacher not in classes_info[0].teacher:
                        classes_info[0].teacher.append(lesson.teacher)
                    if lesson.room not in classes_info[0].room:
                        classes_info[0].room.append(lesson.room)
                else:
                    lesson_info.classes.append(ClassInfo(
                        name=lesson.name,
                        teacher=[lesson.teacher],
                        room=[lesson.room],
                        times=1,
                        cancellations=1 if lesson.canceled else 0,
                        substitutions=1 if lesson.substitution else 0
                    ))
            lesson_info.overall_lessons += len(lessons) - simultaneous_lessons/2
            lesson_info.overall_hours += sum([
                int(les.duration.total_seconds())/3600 for les in lessons
            ]) - simultaneous_lessons/2

        lesson_info.round_numbers()

        return lesson_info
