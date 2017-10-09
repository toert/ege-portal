from django.db import models


class University(models.Model):
    TYPE_GOVERNMENT = 'gov'
    TYPE_MUNICIPAL = 'mun'
    TYPE_PRIVATE = 'ind'

    TYPES = (
        (TYPE_GOVERNMENT, 'Государственный'),
        (TYPE_MUNICIPAL, 'Муниципальный'),
        (TYPE_PRIVATE, 'Частный'),
    )

    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    employment_percentage = models.FloatField()
    average_salary = models.FloatField()
    has_military_department = models.BooleanField(default=False)
    has_dormitory = models.BooleanField(default=False)
    region_name = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=TYPES)

    def __str__(self):
        return '{}'.format(self.name)


class Program(models.Model):
    FORM_FULLTIME = 'fulltime'
    FORM_DISTANCE = 'distance'
    FORM_EXTRAMURAL = 'extramural'
    FORM_MIXED = 'mixed'
    FORM_NIGHT = 'night'

    FORMS = ((FORM_FULLTIME,'Очная'),
             (FORM_DISTANCE, 'Дистанционная'),
             (FORM_EXTRAMURAL, 'Заочная'),
             (FORM_MIXED, 'Очно-заочная'),
             (FORM_NIGHT, 'Вечерняя'))

    LEVEL_BACHELOR = 'bachelor'
    LEVEL_SPECIALTY = 'specialty'

    LEVELS = ((LEVEL_BACHELOR, 'Бакалавриат'),
              (LEVEL_SPECIALTY, 'Специалитет'))

    university = models.ForeignKey(University, related_name='programs')
    average_salary = models.FloatField()
    code = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    cost_per_year = models.PositiveIntegerField()
    custom_exam = models.CharField(max_length=255, blank=True)
    duration = models.PositiveIntegerField()
    employment_percentage = models.FloatField()
    first_passing_score = models.PositiveIntegerField()
    full_name = models.CharField(max_length=255)
    form = models.CharField(max_length=64, choices=FORMS)
    level = models.CharField(max_length=255)
    second_passing_score = models.PositiveIntegerField(blank=True, null=True)
    places = models.PositiveIntegerField()
    ucheba_url = models.CharField(max_length=255)
    year = models.PositiveIntegerField()


class RequiredExam(models.Model):
    EXAM_SOCIAL_STUDIES = 'soc'
    EXAM_GEOGRAPHY = 'geo'
    EXAM_LITERATURE = 'lit'
    EXAM_PHYSICS = 'phy'
    EXAM_HISTORY = 'his'
    EXAM_FOREIGN = 'for'
    EXAM_ICT = 'ict'
    EXAM_RUSSIAN = 'rus'
    EXAM_MATH = 'mat'
    EXAM_CHEMISTRY = 'che'
    EXAM_BIOLOGY = 'bio'

    EXAMS = ((EXAM_SOCIAL_STUDIES, 'Обществознание'),
             (EXAM_GEOGRAPHY, 'География'),
             (EXAM_LITERATURE, 'Литература'),
             (EXAM_PHYSICS, 'Физика'),
             (EXAM_HISTORY, 'История'),
             # ('eng', 'Английский язык'), !!! TODO ADD English as Foreign language
             (EXAM_FOREIGN, 'Иностранный язык'),
             (EXAM_ICT, 'Информатика и ИКТ'),
             (EXAM_RUSSIAN, 'Русский язык'),
             (EXAM_MATH, 'Математика'),
             (EXAM_CHEMISTRY, 'Химия'),
             (EXAM_BIOLOGY, 'Биология'))

    program = models.ForeignKey(Program, related_name='exams')
    exam = models.CharField(max_length=3, choices=EXAMS)

