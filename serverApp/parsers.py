from serverApp.models import Schedule
import random
import re


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

        for current_week_type in json:

            new_dict[weeks_key].append({})
            new_dict[weeks_key][ind_week]['id'] = random.randint(1, 10000)

            # Устанавливаем номер недели.
            if current_week_type == week_type:
                new_dict[weeks_key][ind_week]['number'] = week_number
            else:
                new_dict[weeks_key][ind_week]['number'] = week_number + 1

            new_dict[weeks_key][ind_week]['type'] = current_week_type
            new_dict[weeks_key][ind_week][days_key] = []

            ind_day = 0

            for day in json[str(current_week_type)]:

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

                        # Получаем название.
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['name'] = \
                            self.class_name(period['studyClasses'][0]['studyClassTitle'])

                        # Получаем тип.
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['type'] = \
                            self.class_type(str(period['studyClasses'][0]['studyClassTitle']))

                        # Получаем расположение.
                        class_name = period['studyClasses'][0]['studyClassTitle']
                        class_location_string = period['studyClasses'][0]['studyClassRoom']
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['location'] = \
                            self.class_location(string=class_location_string, name=class_name)

                        # Получаем преподавателя.
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['teacher'] = \
                            period['studyClasses'][0]['studyClassLecturer']
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['teacher_id'] = \
                            random.randint(1, 10000)

                        # Получаем время из номера пары.
                        class_number = list(day['periods']).index(period)
                        time_dict = self.class_time(class_number)
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['start_time'] = \
                            time_dict['start_time']
                        new_dict[weeks_key][ind_week][days_key][ind_day][classes_key][ind_class]['end_time'] = \
                            time_dict['end_time']

                        ind_class += 1

                ind_day += 1

            ind_week += 1

        # Выставляем недели в нужном порядке
        new_dict[weeks_key] = sorted(new_dict[weeks_key], key=lambda x: x['number'])

        return new_dict

    def class_name(self, string):

        # Удаляем сведения о тип занятия.
        start_bracket = str(string).find("(")
        end_bracket = str(string).find(")")
        if start_bracket != -1 and end_bracket != -1:
            name = string[0:start_bracket] + string[end_bracket+2:]
        else:
            name = string

        # Если всё название капсом, то убираем это.
        if name == name.upper():
            name = name.lower()

        # Делаем первое слово с заглавной буквы.
        words = name.split(" ")
        words[0] = str(words[0]).capitalize()
        name = " ".join(words)

        # Физическую культуру любят по-разному писать,
        # поэтому проверим вот таким вот образом и напишем нормально.
        if "физ" in name.lower() and "культ" in name.lower():
            name = "Физическая культура"

        # Иностранный язык всегда обозначается как "ИНО 1/2".
        if "ино" in name.lower() and "1/2" in name.lower():
            name = "Иностранный язык 1/2"

        return name

    def class_location(self, string, name=None):

        if string is None and name is not None:
            if "ино" in name.lower() and "1/2" in name.lower():
                words = name.split(" ")

                for word in words:
                    has_digit = any(ch.isdigit() for ch in word)
                    has_char = any(ch.isalpha() for ch in word)

                    if has_digit and has_char:
                        string = word

        return str(string).lower()

    def class_type(self, string):

        type_string = re.search(r"\((\w+)\)", string)
        type_value = "null"

        if not type_string:
            type_string = string.lower()
        else:
            type_string = str(type_string.group(1)).lower()

        if "лек" in type_string:
            type_value = "lecture"
        elif "лаб" in type_string:
            type_value = "lab"
        elif "сем" in type_string:
            type_value = "seminar"

        return type_value

    def class_time(self, number):

        # Получаем время из номера пары.

        start_time = "null"
        end_time = "null"

        if number == 0:
            start_time = "8:30"
            end_time = "10:15"
        elif number == 1:
            start_time = "10:25"
            end_time = "11:50"
        elif number == 2:
            start_time = "12:00"
            end_time = "13:35"
        elif number == 3:
            start_time = "13:50"
            end_time = "15:25"
        elif number == 4:
            start_time = "15:40"
            end_time = "17:15"
        elif number == 5:
            start_time = "17:25"
            end_time = "19:00"
        elif number == 6:
            start_time = "19:10"
            end_time = "20:45"

        return {"start_time": start_time, "end_time": end_time}
