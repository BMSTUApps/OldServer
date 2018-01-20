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
    day = models.ForeignKey("Day", related_name='classes')

    def __str__(self):
        return "%s (%s) %s-%s" % (self.name, self.location, self.start_time, self.end_time)


class Day(models.Model):
    """ Учебный день """

    class Meta:
        db_table = 'server_app_day'

    # Номер дня в неделе
    number = models.IntegerField()

    def __str__(self):
        return "Учебный день №%i (%i занятий)" % (self.number, self.classes.count())
