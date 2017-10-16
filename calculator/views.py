from django.shortcuts import render
from django.db.models import F
from django.views.generic.detail import DetailView
from django.views.generic import ListView, FormView
from calculator.forms import ExamsForm
from universities.models import RequiredExam, Program

# ExamFormSet = formset_factory(ExamForm, extra=len(RequiredExam.EXAMS))
# some_formset = ExamFormSet(label=[{'id': 'x.id'} for x in some_objects])


def main_page(request):
    if request.method == 'GET':
        return render(request, 'calculator/calculator_page.html',
                      {'score_form': ExamsForm})
    elif request.method == 'POST':
        form = ExamsForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            suitable_programs = Program.objects.prefetch_related('exams', 'university')
            if form_data['city'] != 'all':
                suitable_programs = suitable_programs.filter(university__region_name=form_data['city'])
            if form_data['sort_by'] == 'salary':
                suitable_programs = suitable_programs.order_by(F('average_salary').desc(nulls_last=True))
            else:
                suitable_programs = suitable_programs.order_by('-second_passing_score')

            suitable_programs = \
                [program for program in suitable_programs.filter(custom_exam=None).all() if program.is_suitable(form_data)]
            return render(request, 'calculator/program_list.html',
                          {'programs': suitable_programs})


# class ProgramList(ListView, FormView):
#
#     template_name = 'calculator/program_detail.html'
#     form_class = ExamsForm
#
#     def get_queryset(self):
#         self.publisher = get_object_or_404(Publisher, name=self.args[0])
#         return Book.objects.filter(publisher=self.publisher)
#

class ProgramDetailView(DetailView):
    model = Program
    context_object_name = 'program'
    template_name = 'calculator/program_detail.html'

"""
# TODO 
1. Университет детаилс
2. Поиск?
3. 
"""