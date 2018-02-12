from django.views.generic import View
from django.http import HttpResponse

import json
import math

from serverApp.managers import ScheduleManager

# Создавать менеджер тут не надо, он будет один на приложение и создаваться автоматически совсем в другом месте.
manager = ScheduleManager()


# Экранированный запрос
class ScheduleView(View):

    def get(self, request):

        group_string = str(request.GET.get("group"))

        # Получаем данные из названия группы.
        groups_elements = group_string.split("-")
        faculty = ''.join(i for i in groups_elements[0] if not i.isdigit())
        department = int(''.join(i for i in groups_elements[0] if i.isdigit()))
        group = int(groups_elements[-1])
        course = int(math.ceil(int(group/10)/2.0))

        # Запрос на "raspisanie.bmstu.ru".
        response = manager.loader.load_schedule(faculty=faculty, department=department, course=course, group=group)

        # Для теста
        #response = manager.loader.load_test_schedule()

        # Парсинг
        week_number = manager.current_week_number()
        week_type = manager.current_week_type()
        parsed_response = manager.parser.parse(json=response, group=group_string, week_number=week_number, week_type=week_type)

        return HttpResponse(
            json.dumps(parsed_response, ensure_ascii=False),
            content_type="application/json"
        )


class WeekView(View):

    def get(self, request):

        response = {"week_number": manager.current_week_number(), "week_type": manager.current_week_type()}

        return HttpResponse(
            json.dumps(response, ensure_ascii=False),
            content_type="application/json"
        )
