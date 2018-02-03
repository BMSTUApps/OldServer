import requests
import json
from BMSTUScheduleServer import settings

# TODO: Сделать класс запроса, содержащий ошибку и код ответа.


class BaseLoader:

    def __init__(self, host_address, port):

        self.host_address = host_address
        self.port = port

    def compose_url(self, method="", params={}):

        # Собираем базовый URL
        url = "%s:%s/%s" % (self.host_address, self.port, method)

        # Если есть параметры, добавляем их к URL'у.
        if len(params) > 0:
            url += "?"

            for param, value in params.items():
                url += "%s=%s&" % (param, value)

            # Удаляем последний ненужный '&'.
            url = url[:-1]

        return url

    def make_request(self, url):

        # Делаем запрос
        request = requests.get(url)

        # Возвращаем JSON
        return request.json()


class ScheduleLoader(BaseLoader):

    def __init__(self):

        self.host_address = "http://raspisanie.bmstu.ru"
        self.port = 8088

    def load_schedule(self, faculty, department, course, group):

        # Генерируем строку запроса
        params = {"faculty": faculty, "department": department, "course": course, "groupNumber": group}
        url = self.compose_url(method="api/timetable/get/now/param", params=params)

        # Делаем запрос
        json = self.make_request(url)

        return json

    def load_test_schedule(self):

        response_path = settings.TEMPLATE_DIRS[0] + "schedule_response.json"

        with open(response_path) as json_data:
            response = json.load(json_data)

        return response

    def load_faculties(self):

        url = self.compose_url(method="api/faculties/get/now/all")
        json = self.make_request(url)

        return json

    def load_departments(self, faculty):

        params = {"faculty": faculty}
        url = self.compose_url(method="api/departments/get/now/param", params=params)
        json = self.make_request(url)

        return json

    def load_groups(self, faculty, department, course):

        params = {"faculty": faculty, "department": department, "course": course}
        url = self.compose_url(method="api/studygroup/get/now/param", params=params)
        json = self.make_request(url)

        return json

    def load_week(self):

        url = self.compose_url(method="api/semester/get/now/weeknumber")
        json = self.make_request(url)

        return json
