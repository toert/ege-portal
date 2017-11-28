from django.shortcuts import render
from django.db.models import F
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, FormView
from calculator.forms import ExamsForm
from universities.models import University, Program

BANNED_UNIVERSITIES_IDS = ['80E3C5967821518B3168DAEF7B105D8B',
                           'E8AA0ECD1A1C1761442C1E88BB712491',
                           '031B8ADE96593077E0FD925F8CFB7DA5',
                           '3128A297ED66FF1ADE82BBB57FA001A6',
                           '3AE6CD0CCC7ACC85296C0CF157D3FABF',
                           '4165BC2E997EA24FD0DF725F0A6F91E7',
                           '4BD0DFBBB287CB0534EC032AE477C5CE',
                           '7079EB8CE1313CB0ABE5E728AF737707']


class UniversitiesList(ListView):

    model = University
    context_object_name = 'universities'
    template_name = 'rating/top_universities.html'
    #paginate_by = 30


    def get_queryset(self):
        return University.objects.exclude(graduate_id__in=BANNED_UNIVERSITIES_IDS)\
            .order_by('region_name', '-average_salary').all()