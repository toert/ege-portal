from django import forms
from universities.models import RequiredExam


class ExamsForm(forms.Form):
    for code, exam_name in RequiredExam.EXAMS:
        exec('{} = forms.IntegerField(100, 0, label="{}", required=False)'.format(code, exam_name))


# class ExamForm(forms.Form):
#     exam = forms.IntegerField(100, 0)
#
#     def __init__(self, *args, **kwargs):
#         super(ExamForm, self).__init__(*args, **kwargs)
#         self.fields['exam'].label = kwargs['label']
#
