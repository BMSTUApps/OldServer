from serverApp.schedule_loader import ScheduleLoader
from serverApp.schedule_parser import ScheduleParser


class ScheduleManager:

    def __init__(self):
        self.loader = ScheduleLoader()
        self.parser = ScheduleParser()
