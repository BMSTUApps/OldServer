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
