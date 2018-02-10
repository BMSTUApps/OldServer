from django.views.generic import View
from django.http import HttpResponse

import json

from serverApp.managers import ScheduleManager


# Тестовая страница
class MainView(View):

    def get(self, request):

        # Создавать менеджер тут не надо, он будет один на приложение и создаваться автоматически совсем в другом месте.
        manager = ScheduleManager()

        # Реальный запрос на "raspisanie.bmstu.ru".
        response = manager.loader.load_schedule(faculty="ИУ", department=5, course=3, group=53)
        print("Ответ сервака: " + str(response))

        # Тестовый запрос
        test_response = manager.loader.load_test_schedule()
        print("Тест: " + str(test_response))

        #print("Парсинг..")
        #response_dict = manager.parser.parse(json=test_response)
        #print("Числитель: " + str(response_dict["nominator"]))
        #print("Знаменатель: " + str(response_dict["denominator"]))

        return HttpResponse(
            json.dumps(response, ensure_ascii=False),
            content_type="application/json"
        )
