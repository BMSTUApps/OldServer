from django.views.generic import View
from django.http import HttpResponse

import json

from serverApp.managers import ScheduleManager


# Тестовая страница
class MainView(View):

    def get(self, request):

        # Создавать менеджер тут не надо, он будет один на приложение и создаваться автоматически совсем в другом месте.
        manager = ScheduleManager()
        response = manager.loader.load_schedule(faculty="ИУ", department=5, course=3, group=53)

        print("Ответ сервака: " + str(response))

        test1 = manager.loader.load_faculties()
        print("Тестовый запрос 1: " + str(test1))

        test2 = manager.loader.load_departments(faculty="ИУ")
        print("Тестовый запрос 2: " + str(test2))

        test3 = manager.loader.load_groups(faculty="ИУ", department=5, course=3)
        print("Тестовый запрос 3: " + str(test3))

        test4 = manager.loader.load_week()
        print("Тестовый запрос 4: " + str(test4))

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
