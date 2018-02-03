from serverApp import models


class ScheduleParser:

    def __init__(self, json={}):
        self.schedule_json = json

    # разбиваем недели на числители и знаменатели
    def parse(self):
        json = self.schedule_json
        whole_week = json[0]['studyWeek']
        nominator = whole_week[:]
        denominator = whole_week[:]

        for day in whole_week:
            for period in day['periods']:
                for studyClass in period['studyClasses']:
                    if studyClass['type'] == 'nominator':
                        denominator[whole_week.index(day)]['periods'][day['periods'].index(period)]['studyClasses'][
                            period['studyClasses'].index(studyClass)] = {}
                    elif studyClass['type'] == 'denominator':
                        nominator[whole_week.index(day)]['periods'][day['periods'].index(period)]['studyClasses'][
                            period['studyClasses'].index(studyClass)] = {}

        return [nominator, denominator]
