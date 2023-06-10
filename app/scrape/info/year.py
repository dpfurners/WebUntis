import datetime

from app.scrape.data import Day, Lesson, Week


def year_lesson_info(day: Day, dt: datetime.datetime = None):
    """
    overall-lessons: the overall lesson count
    canceled-lessons: the canceled lesson count
    substitution-lessons: the substitution lesson count
    similar-lessons: the similar lesson count
    """
    lessons = day.lessons
    if dt:
        lessons = [les for les in lessons if dt <= les.end]
    simultaneous_lessons = 0
    canceled_lessons = len([les for les in lessons if les.canceled])
    substitution_lessons = len([les for les in lessons if les.substitution])
    for lesson in lessons:
        if simultaneous_les := [les for les in lessons if les.start == lesson.start and les.end == lesson.end]:
            simultaneous_lessons += len(simultaneous_les) - 1
    return {
        "overall-lessons": len(lessons) - simultaneous_lessons/2,
        "canceled-lessons": canceled_lessons,
        "substitution-lessons": substitution_lessons,
        "similar-lessons": None}


def year_lessons_overview(day: Day, dt: datetime.datetime = None):
    lessons = []
    for les in day.lessons:
        if dt and (dt >= les.end):
            continue
        if les.name in [ln.name for ln in lessons] and \
                les.start in [ls.start for ls in lessons] and \
                les.end in [le.end for le in lessons]:
            continue
        lessons.append(les)
    return [lesn.name for lesn in lessons]


def year_info(day: Day, dt: datetime.datetime = None):
    return {
        "date": {
            "day": day.date,
            "time": dt.strftime("%H:%M") if isinstance(dt, datetime.datetime) else "all",
            "week": day.date.isocalendar().week,
            "weekday": day.date.strftime("%A")},
        "lesson-info": year_lesson_info(day, dt),
        "lesson-overview": year_lessons_overview(day, dt),
    }
