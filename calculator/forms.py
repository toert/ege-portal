from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from universities.models import RequiredExam, Program, University


class ExamsForm(forms.Form):
    rus = forms.IntegerField(100, 34, label="Русский язык", required=False)
    mat = forms.IntegerField(100, 27, label="Математика", required=False)
    soc = forms.IntegerField(100, 40, label="Обществознание", required=False)
    phy = forms.IntegerField(100, 36, label="Физика", required=False)
    his = forms.IntegerField(100, 29, label="История", required=False)
    bio = forms.IntegerField(100, 36, label="Биология", required=False)
    che = forms.IntegerField(100, 36, label="Химия", required=False)
    lan = forms.IntegerField(100, 22, label="Иностранный язык", required=False)
    ict = forms.IntegerField(100, 40, label="Информатика и ИКТ", required=False)
    geo = forms.IntegerField(100, 40, label="География", required=False)
    lit = forms.IntegerField(100, 32, label="Литература", required=False)

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
        self.fields['is_custom_exam_taken'].widget.attrs['class'] += ' custom-control-input'

    def exams(self):
        existed_exams = [slug for name, slug in RequiredExam.EXAMS]
        print([field for slug, field in self.fields.items()])
        return [field for slug, field in self.fields.items() if slug in existed_exams]

    def other_fields(self):
        existed_exams = [slug for name, slug in RequiredExam.EXAMS]
        return filter(lambda field: field not in existed_exams, self.fields)