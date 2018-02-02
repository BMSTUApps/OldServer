import requests


class ScheduleLoader:

    def __init__(self):
        self.api_address = "http://raspisanie.bmstu.ru:8088/api/"

    def load_schedule(self, faculty, department, course, group):

        # Генерируем строку запроса
        request_string = self.api_address + "timetable/get/now/param?faculty=%s&department=%s&course=%s&groupNumber=%s" % (faculty, department, course, group)

        # Делаем запрос
        request = requests.get(request_string)
        print("Делаем запрос " + request_string)

        return request.json()

    def load_faculties(self):

        request_string = self.api_address + "faculties/get/now/all"
        request = requests.get(request_string)

        return request.json()

    def load_departments(self, faculty):

        request_string = self.api_address + "departments/get/now/param?faculty=%s" % faculty
        request = requests.get(request_string)

        return request.json()

    def load_groups(self, faculty, department, course):

        request_string = self.api_address + "studygroup/get/now/param?faculty=%s&department=%s&course=%s" % (faculty, department, course)
        request = requests.get(request_string)

        return request.json()

    def load_week(self):

        request_string = self.api_address + "semester/get/now/weeknumber"
        request = requests.get(request_string)

        return request.json()
