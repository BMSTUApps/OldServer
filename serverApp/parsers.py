from serverApp.models import Schedule
import random


class ScheduleParser:

    def parse(self, json, group, week_number, week_type):

        # JSON Layer

        # Разбиваем все занятия на две недели (числитель и знаменатель).
        json = self.divide(json=json)

        # Удаляем ненужные символы.
        json = self.remove_symbols(json=json)

        # Models Layer

        # Пока не готова БД уровня с моделями не будет.
        # Поэтому на этом уровне мы будем видоизменять JSON в нужный вид.
        # Подробности тут - github.com/BMSTUScheduleTeam/BMSTUScheduleServer/issues/9

        json = self.transform_json(json=json, group=group, week_number=week_number, week_type=week_type)

        return json

    def divide(self, json):

        # Проверяем на пустой json.
        json_list = list(json)
        if len(json_list) == 0:
            return {"numerator": [], "denominator": []}

        days = json[0]['studyWeek']

        # Разбиваем все занятия на две недели (числитель и знаменатель).

        nominator_days = []
        denominator_days = []

        for day in days:

            periods = day["periods"]
            nominator_periods = []
            denominator_periods = []

            for period in periods:

                study_classes = period["studyClasses"]
                nominator_classes = []
                denominator_classes = []

                for study_class in study_classes:

                    study_class_type = study_class["type"]

                    if study_class_type == "nominator":
                        nominator_classes.append(study_class)

                    elif study_class_type == "denominator":
                        denominator_classes.append(study_class)

                    else:
                        nominator_classes.append(study_class)
                        denominator_classes.append(study_class)

                nominator_period = dict(period)
                nominator_period["studyClasses"] = nominator_classes
                nominator_periods.append(nominator_period)

                denominator_period = dict(period)
                denominator_period["studyClasses"] = denominator_classes
                denominator_periods.append(denominator_period)

            nominator_day = dict(day)
            nominator_day["periods"] = nominator_periods
            nominator_days.append(nominator_day)

            denominator_day = dict(day)
            denominator_day["periods"] = denominator_periods
            denominator_days.append(denominator_day)

        return {"numerator": nominator_days, "denominator": denominator_days}

    def remove_symbols(self, json):

        # Удаляем ненужные символы из json'а.

        # Если словарь
        if isinstance(json, dict):

            for key, item in json.items():
                if isinstance(item, str):
                    json[key] = self.remove_symbols_from_item(string=item)
                elif isinstance(item, dict):
                    json[key] = self.remove_symbols(json=item)
                elif isinstance(item, list):
                    json[key] = self.remove_symbols(json=item)
                else:
                    continue

        # Если список
        elif isinstance(json, list):

            for index, item in enumerate(json):
                if isinstance(item, str):
                    json[index] = self.remove_symbols_from_item(string=item)
                elif isinstance(item, dict):
                    json[index] = self.remove_symbols(json=item)
                elif isinstance(item, list):
                    json[index] = self.remove_symbols(json=item)
                else:
                    continue

        return json

    def remove_symbols_from_item(self, string):

        # Удаляем ненужные символы из строки.

        # Удаляем "null"
        string = string.replace("null", "")

        # Удаляем "\xa0"
        string = string.replace("\xa0", " ")

        # Удаляем больше одного пробела.
        string = string.replace("  ", " ")
        string = string.replace("   ", " ")

        # Удаляем пробелы на концах строки.
        if string[0] == " ":
            string = string[1:]
        if string[-1] == " ":
            string = string[:-1]

        # Первые буквы слов делаем заглавными.
        string = string.title()

        return string

    def create_model(self, json):

        # Создаем модель расписания из json'а.

        schedule = Schedule()

        # Заполняем модель

        return schedule

    def transform_json(self, json, group, week_number, week_type):

        # Метод для преобразования расписания в нужный формат.

        weeks_key = "weeks"
        days_key = "days"
        group_key = "group"
        classes_key = "classes"

        new_dict = dict()
        new_dict[group_key] = group
        new_dict[weeks_key] = []

        ind_week = 0

        for week_type in json:

            new_dict[weeks_key].append({})
            new_dict[weeks_key][ind_week]['id'] = random.randint(1, 10000)
            new_dict[weeks_key][ind_week]['number'] = random.randint(1, 10000)
            new_dict[weeks_key][ind_week]['type'] = week_type
            new_dict[weeks_key][ind_week][days_key] = []

            ind_day = 0

            for day in json[str(week_type)]:

                new_dict[weeks_key][ind_week][days_key].append({})
                new_dict[weeks_key][ind_week][days_key][ind_day]['id'] = random.randint(1, 10000)
                new_dict[weeks_key][ind_week][days_key][ind_day]['name'] = day['title']
                new_dict[weeks_key][ind_week][days_key][ind_day][classes_key] = []

                ind_class = 0

                for period in day['periods']:

                    if len(period['studyClasses']) > 0:

                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key].append({})

                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['id'] = \
                            random.randint(1, 10000)
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['name'] = \
                            period['studyClasses'][0]['studyClassTitle']
                        # В скобках обычно пишут тип занятия
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['type'] = \
                            str(period['studyClasses'][0]['studyClassTitle']).split(' ')[0]
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['location'] = \
                            period['studyClasses'][0]['studyClassRoom']
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['teacher'] = \
                            period['studyClasses'][0]['studyClassLecturer']
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['teacher_id'] = \
                            random.randint(1, 10000)
                        # Пока что решил не запариваться, накидать до кучи время начала занятия
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['start_time'] = \
                            random.randint(1, 10000)
                        # Пока что решил не запариваться, накидать до кучи время окончания занятия
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['end_time'] = \
                            random.randint(1, 10000)

                        ind_class += 1

                ind_day += 1

            ind_week += 1

        return new_dict