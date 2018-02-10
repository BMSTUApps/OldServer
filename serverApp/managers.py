from serverApp.loaders import ScheduleLoader
from serverApp.parsers import ScheduleParser

import datetime
import math


class ScheduleManager:

    def __init__(self):
        self.loader = ScheduleLoader()
        self.parser = ScheduleParser()

    def current_week_number(self):

        # Пока захардкожу даты, но в будущем они будут хранится в БД.
        start_date = datetime.datetime(2018, 2, 5)  # числитель
        end_date = datetime.datetime(2018, 6, 3)

        # Определяем номер недели.
        now = datetime.datetime.now()
        delta = now - start_date
        week_number = math.ceil((delta.days + 1) / 7.0)
        if now > end_date:
            week_number = 17

        return week_number

    def current_week_type(self):

        # Определяем тип недели.
        week_type = "numerator"
        if self.current_week_number() % 2 == 0:
            week_type = "denominator"

        return week_type
