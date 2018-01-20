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
    # teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL)

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
