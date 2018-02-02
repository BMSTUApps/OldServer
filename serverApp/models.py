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
    teacher = models.ForeignKey("Teacher", related_name='classes', on_delete=models.PROTECT)

    # Тип: лаба/семинар/лекция
    type = models.CharField(max_length=30)

    # Время начала занятия
    start_time = models.TimeField()

    # Время окончания занятия
    end_time = models.TimeField()

    # День (необходим для связи в БД)
    day = models.ForeignKey("Day", related_name='classes', on_delete=models.PROTECT)
    
    def __init__(self, json):
        super(Class, self).__init__()
        self.location = str(json['studyClassRoom'])
        self.name = str(json['studyClassTitle'])

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
        return "Учебная неделя (%i учебных дней)" % (self.days.count())


class Schedule(models.Model):
    """ Расписание """

    class Meta:
        db_table = 'server_app_schedule'

    # Группа
    group = models.ForeignKey("Group", related_name='schedule', on_delete=models.PROTECT)

    # TODO: Я хз пока что, как правильно сделать связи, чтобы было два массива дней. Видимо надо делать свойство у недели, которое будет показывать числитель это или знаменатель.

    # Неделя числителя (необходима для связи в БД)
    # numerator = models.ForeignKey("Week", related_name='numerator', on_delete=models.PROTECT)

    # Неделя знаменателя (необходима для связи в БД)
    # denominator = models.ForeignKey("Week", related_name='denominator', on_delete=models.PROTECT)

    def __str__(self):
        return "Учебная неделя (%i учебных дней)" % (self.days.count())


class Faculty(models.Model):
    """ Факультет """

    class Meta:
        db_table = 'server_app_faculty'

    # Название факультета
    name = models.CharField(max_length=50)

    # Сокращённое название факультета
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return "Факультет {} ({})".format(self.name, self.short_name)


class Department(models.Model):
    """ Кафедра """

    class Meta:
        db_table = 'server_app_department'

    # Название кафедры
    name = models.CharField(max_length=50)

    # Сокращённое название кафедры
    short_name = models.CharField(max_length=15)

    # Факультет
    faculty = models.ForeignKey("Faculty", related_name='department', on_delete=models.PROTECT)

    def __str__(self):
        return "Кафедра {} ({})".format(self.name, self.short_name)


class Group(models.Model):
    """ Группа """

    class Meta:
        db_table = 'server_app_group'

    # Кафедра, на которой обучается группа
    department = models.ForeignKey('Department', related_name='group', on_delete=models.PROTECT)

    # На каком курсе группа
    course = models.CharField(max_length=15)

    # Сокращённое название группы
    short_name = models.CharField(max_length=15)

    def __str__(self):
        return "Группа {}".format(self.short_name)


class Teacher(models.Model):
    """ Преподаватель """

    class Meta:
        db_table = 'server_app_teacher'

    # Фотка препода (пока что хз насчёт того, куда будет подгружаться, пока без upload_to)
    image = models.ImageField(null=True)

    # Имя препода
    first_name = models.CharField(max_length=30)

    # Фамилия препода
    last_name = models.CharField(max_length=30)

    # Отчество препода
    middle_name = models.CharField(max_length=30)

    # Повадки препода, особенности поведения (будет браться с бомонки.нет)
    description = models.CharField(max_length=150)

    def __init__(self, json):
        models.Model.__init__(self)
        self.last_name = str(json['studyClassLecturer']).split(' ')[0]

    def __str__(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)
