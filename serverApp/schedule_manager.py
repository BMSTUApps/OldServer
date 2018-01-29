from serverApp import models
from serverApp import schedule_loader


class ScheduleManager:

    def __init__(self):
        self.loader = ScheduleLoader()
        self.parser = "Parser"
