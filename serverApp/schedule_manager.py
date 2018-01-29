from serverApp import models
from serverApp import schedule_loader
from serverApp import schedule_parser


class ScheduleManager:

    def __init__(self):
        self.loader = ScheduleLoader()
        self.parser = ScheduleParser()
