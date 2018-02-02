from django.shortcuts import render
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

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
