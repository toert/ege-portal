from django.shortcuts import render

from calculator.forms import ExamsForm
from universities.models import RequiredExam, Program
from django.views.generic.edit import FormView
from django.forms import formset_factory

# ExamFormSet = formset_factory(ExamForm, extra=len(RequiredExam.EXAMS))
# some_formset = ExamFormSet(label=[{'id': 'x.id'} for x in some_objects])


def main_page(request):
    if request.method == 'GET':
        return render(request, 'calculator/calculator_page.html',
                      {'score_form': ExamsForm})
    elif request.method == 'POST':
        form = ExamsForm(request.POST)
        if form.is_valid():
            selected_exams = [exam for exam, score in form.cleaned_data.items() if score]
            score_sum = sum([score for exam, score in form.cleaned_data.items() if score])
            suitable_programs_by_score = Program.objects.filter(second_passing_score__lte=score_sum)\
                .filter(custom_exam=None).order_by('-second_passing_score').all()
            suitable_programs = []
            for program in suitable_programs_by_score:
                if all(exam in selected_exams for exam in program.exams_as_list):
                    suitable_programs.append(program)

            return render(request, 'calculator/program_list.html',
                          {'programs': suitable_programs})

"""
# TODO 
1. Сколько запросов к БД?
2. Написать Борисычу про функционал
3. Сделать as_string
4. Поддержку городов
5. Форматирование зарплаты

"""