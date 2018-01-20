from django.db import models


""" Стэк расписания """


class Class(models.Model):
    """ Занятие """

    class Meta:
        db_table = 'server_app_class'

    # Название
    name = models.CharField(max_length=255)

    # Аудитория / место занятия (например, СК)
    location = models.CharField(max_length=30)

    # Преподаватель
    # FIXME: Нужно расскоментировать, когда появится Teacher
    # teacher = models.ForeignKey("Teacher", related_name='classes', on_delete=models.PROTECT)

    # Тип: лаба/семинар/лекция
    type = models.CharField(max_length=30)

    # Время начала занятия
    start_time = models.TimeField()

    # Время окончания занятия
    end_time = models.TimeField()

    # День (необходим для связи в БД)
    day = models.ForeignKey("Day", related_name='classes', on_delete=models.PROTECT)

    def __str__(self):
        return "%s (%s) %s-%s" % (self.name, self.location, self.start_time, self.end_time)


class Day(models.Model):
    """ Учебный день """

    class Meta:
        db_table = 'server_app_day'

    # Номер дня в неделе
    number = models.IntegerField()

    # Неделя (необходима для связи в БД)
    week = models.ForeignKey("Week", related_name='days', on_delete=models.PROTECT)

    def __str__(self):
        return "Учебный день №%i (%i занятий)" % (self.number, self.classes.count())


class Week(models.Model):
    """ Учебный неделя """

    class Meta:
        db_table = 'server_app_week'

    # Тип: числитель/знаменатель
    type = models.CharField(max_length=30)

    def __str__(self):
        return "Учебный неделя (%i учебных дней)" % (self.days.count())


class Schedule(models.Model):
    """ Расписание """

    class Meta:
        db_table = 'server_app_schedule'

    # Группа
    # FIXME: Нужно расскоментировать, когда появится Group
    # group = models.ForeignKey("Group", related_name='schedule', on_delete=models.PROTECT)

    # TODO: Я хз пока что, как правильно сделать связи, чтобы была два массива дней. Видимо надо делать свойство у недели, которое будет показывать числитель это или знаменатель.

    # Неделя числителя (необходима для связи в БД)
    # numerator = models.ForeignKey("Week", related_name='numerator', on_delete=models.PROTECT)

    # Неделя знаменателя (необходима для связи в БД)
    # denominator = models.ForeignKey("Week", related_name='denominator', on_delete=models.PROTECT)

    def __str__(self):
        return "Учебный неделя (%i учебных дней)" % (self.days.count())
