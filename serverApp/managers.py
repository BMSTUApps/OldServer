from serverApp.loaders import ScheduleLoader
from serverApp.parsers import ScheduleParser


class ScheduleManager:

    def __init__(self):
        self.loader = ScheduleLoader()
        self.parser = ScheduleParser()
