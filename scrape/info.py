from .data import Day, Lesson, Week


def day_lesson_info(day: Day):
    """
    overall-lessons: the overall lesson count
    canceled-lessons: the canceled lesson count
    substitution-lessons: the substitution lesson count
    similar-lessons: the similar lesson count
    """
    simultaneous_lessons = 0
    canceled_lessons = len([les for les in day.lessons if les.canceled])
    substitution_lessons = len([les for les in day.lessons if les.substitution])
    for lesson in day.lessons:
        if simultaneous_les := [les for les in day.lessons if les.start == lesson.start and les.end == lesson.end]:
            simultaneous_lessons += len(simultaneous_les) - 1
    return {
        "overall-lessons": len(day.lessons) - simultaneous_lessons/2,
        "canceled-lessons": canceled_lessons,
        "substitution-lessons": substitution_lessons,
        "similar-lessons": None}


def day_lessons_overview(day: Day):
    lessons = []
    for les in day.lessons:
        if les.name in [ln.name for ln in lessons] and \
                les.start in [ls.start for ls in lessons] and \
                les.end in [le.end for le in lessons]:
            continue
        lessons.append(les)
    return [lesn.name for lesn in lessons]


def day_info(day: Day):
    return {
        "date": {
            "day": day.date,
            "week": day.date.isocalendar().week,
            "weekday": day.date.strftime("%A")},
        "lesson-info": day_lesson_info(day),
        "lesson-overview": day_lessons_overview(day),
        "lessons": day.lessons
    }
