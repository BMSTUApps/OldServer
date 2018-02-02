from serverApp import models


class ScheduleParser:

    def __init__(self, json={}):
        self.schedule_json = json

    # разбиваем недели на числители и знаменатели
    def parse(self):
        json = self.schedule_json
        whole_week = json['studyWeek']
        nominator = denominator = whole_week

        for day in whole_week:
            for period in day['periods']:
                class_type = str(period['studyClasses'][0]['type'])
                if class_type == 'normal':
                    pass
                elif class_type == 'nominator':
                    denominator[day]['periods'][period]['studyClasses'] = []
                elif class_type == 'denominator':
                    nominator[day]['periods'][period]['studyClasses'] = []
