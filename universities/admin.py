from django.contrib import admin
from universities.models import Program, University, RequiredExam


class ExamInline(admin.TabularInline):
    model = RequiredExam


class ProgramInline(admin.TabularInline):
    model = Program


class ProgramAdmin(admin.ModelAdmin):
    inlines = [ExamInline]


class UniversityAdmin(admin.ModelAdmin):
    inlines = [ProgramInline]


admin.site.register(University, UniversityAdmin)
admin.site.register(Program, ProgramAdmin)
