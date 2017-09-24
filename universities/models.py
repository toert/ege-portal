from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    employment_percentage = models.FloatField()
    average_salary = models.FloatField()
    has_military_department = models.BooleanField(default=False)
    has_dormitory = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)


class Faculty(models.Model):
    university = models.ForeignKey(University, related_name='faculties')
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class Program(models.Model):
    faculty = models.ForeignKey(Faculty, related_name='programs')
    year = models.PositiveIntegerField()
    # Postuplenie
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    first_passing_score = models.PositiveIntegerField()
    second_passing_score = models.PositiveIntegerField(blank=True, null=True)
    # Graduate
    average_salary = models.FloatField()
    employment_percentage = models.FloatField()
    average_age = models.PositiveIntegerField()


class Exam(models.Model):
    name = models.CharField(max_length=255)
    minimal_score = models.IntegerField()
    year = models.PositiveIntegerField()


class RequiredExam(models.Model):
    program = models.ForeignKey(Program, related_name='exams')
    exam = models.ForeignKey(Exam, related_name='programs')

