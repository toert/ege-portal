from django.shortcuts import render
from django.db.models import F
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, FormView
from calculator.forms import ExamsForm
from universities.models import University, Program


def calculator_page(request):
    if request.method == 'GET':
        return render(request, 'calculator/calculator_page.html',
                      {'score_form': ExamsForm})


class ProgramsCalculator(ListView):
    model = Program
    context_object_name = 'programs'
    paginate_by = 15
    template_name = 'calculator/calc_result.html'

    def get_queryset(self):
        suitable_programs = Program.objects.prefetch_related('exams', 'university')
        if self.request.GET['city'] != 'all':
            suitable_programs = suitable_programs.filter(university__region_name=self.request.GET['city'])
        if self.request.GET['sort_by'] == 'salary':
            suitable_programs = suitable_programs.order_by(F('average_salary').desc(nulls_last=True))
        else:
            suitable_programs = suitable_programs.order_by('-second_passing_score')
        if not self.request.GET.get('is_custom_exam_taken', None):
            suitable_programs = suitable_programs.filter(custom_exam=None)
        suitable_programs = [program for program in suitable_programs.all() if program.is_suitable(self.request.GET)]
        return suitable_programs


class ProgramDetailView(DetailView):
    model = Program
    context_object_name = 'program'
    template_name = 'calculator/program_detail.html'


class UniversityDetailView(DetailView):
    model = University
    context_object_name = 'university'
    template_name = 'calculator/university_detail.html'

"""
# TODO 
2. Поиск?
3. Хранить аббревиатуры и альтернативные названия
5. FBV to CBV & rename it
"""