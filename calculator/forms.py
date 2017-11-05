from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from universities.models import RequiredExam, Program, University


class ExamsForm(forms.Form):
    soc = forms.IntegerField(100, 40, label="Обществознание", required=False)
    geo = forms.IntegerField(100, 40, label="География", required=False)
    lit = forms.IntegerField(100, 32, label="Литература", required=False)
    phy = forms.IntegerField(100, 36, label="Физика", required=False)
    his = forms.IntegerField(100, 29, label="История", required=False)
    lan = forms.IntegerField(100, 22, label="Иностранный язык", required=False)
    ict = forms.IntegerField(100, 40, label="Информатика и ИКТ", required=False, initial=100)
    rus = forms.IntegerField(100, 34, label="Русский язык", required=False, initial=100)
    mat = forms.IntegerField(100, 27, label="Математика", required=False, initial=100)
    che = forms.IntegerField(100, 36, label="Химия", required=False)
    bio = forms.IntegerField(100, 36, label="Биология", required=False)

    is_custom_exam_taken = forms.BooleanField(required=False, label="Готовы сдавать внутренние испытания ВУЗов?")
    sort_by = forms.ChoiceField(choices=[('salary', 'Зарплате'), ('score', 'Проходному баллу')], label='Сортировать по',
                                widget=forms.RadioSelect, initial='salary')

    def __init__(self, *args, **kwargs):
        super(ExamsForm, self).__init__(*args, **kwargs)
        available_regions = set(University.objects.values_list('region_name', flat=True))
        self.fields['city'] = forms.ChoiceField(
            choices=reversed([(region, region) for region in available_regions] + [('all', 'Все')]),
            label='Город'
        )
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control score'

