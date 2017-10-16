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

    average_salary = models.FloatField()
    employment_percentage = models.FloatField()
    graduate_id = models.CharField(max_length=255)
    has_military_department = models.BooleanField(default=False)
    has_dormitory = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    region_name = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=TYPES)
    ucheba_url = models.CharField(max_length=255)
    year = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.name)


class Program(models.Model):
    FORM_FULLTIME = 'fulltime'
    FORM_DISTANCE = 'distance'
    FORM_EXTRAMURAL = 'extramural'
    FORM_MIXED = 'mixed'
    FORM_NIGHT = 'night'

    FORMS = ((FORM_FULLTIME,'очная'),
             (FORM_DISTANCE, 'дистанционная'),
             (FORM_EXTRAMURAL, 'заочная'),
             (FORM_MIXED, 'очно-заочная'),
             (FORM_NIGHT, 'вечерняя'))

    LEVEL_BACHELOR = 'bachelor'
    LEVEL_SPECIALTY = 'specialty'

    LEVELS = ((LEVEL_BACHELOR, 'бакалавриат'),
              (LEVEL_SPECIALTY, 'специалитет'))

    university = models.ForeignKey(University, related_name='programs')
    average_salary = models.FloatField(null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    common_name = models.CharField(max_length=255)
    cost_per_year = models.PositiveIntegerField(null=True, blank=True)
    custom_exam = models.CharField(max_length=511, blank=True, null=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    employment_percentage = models.FloatField(blank=True, null=True)
    first_passing_score = models.PositiveIntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=255)
    form = models.CharField(max_length=64, choices=FORMS)
    level = models.CharField(max_length=255)
    second_passing_score = models.PositiveIntegerField(blank=True, null=True)
    places = models.PositiveIntegerField(null=True)
    ucheba_url = models.CharField(max_length=255)
    year = models.PositiveIntegerField()

    @property
    def exams_as_list(self):
        required_exams_for_program = self.exams.all()
        return [ex.exam for ex in required_exams_for_program]

    @property
    def exams_as_string(self):
        named_slugs = dict(RequiredExam.EXAMS)
        return ', '.join([named_slugs[slug] for slug in self.exams_as_list])

    def is_suitable(self, exam_form_data):
        required_exams = self.exams_as_list
        selected_exams = [exam for exam, score in exam_form_data.items() if score]
        selected_score = sum([score for exam, score in exam_form_data.items() if score and exam in required_exams])
        if all(exam in selected_exams for exam in required_exams) and self.second_passing_score:
            if selected_score >= self.second_passing_score:
                return True
        return False


class RequiredExam(models.Model):
    EXAM_SOCIAL_STUDIES = 'soc'
    EXAM_GEOGRAPHY = 'geo'
    EXAM_LITERATURE = 'lit'
    EXAM_PHYSICS = 'phy'
    EXAM_HISTORY = 'his'
    EXAM_FOREIGN = 'lan'
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
             (EXAM_FOREIGN, 'Иностранный язык'),
             (EXAM_ICT, 'Информатика и ИКТ'),
             (EXAM_RUSSIAN, 'Русский язык'),
             (EXAM_MATH, 'Математика'),
             (EXAM_CHEMISTRY, 'Химия'),
             (EXAM_BIOLOGY, 'Биология'))

    program = models.ForeignKey(Program, related_name='exams')
    exam = models.CharField(max_length=3, choices=EXAMS)

