import datetime
from dataclasses import dataclass

from app.scrape.data import Week
from app.scrape.info.model import InfoCollection


@dataclass
class WeekInfo(InfoCollection):

    def __init__(self, week: Week):
        super().__init__(*week)


def week_info(day: Week) -> WeekInfo:
    return WeekInfo(day)
