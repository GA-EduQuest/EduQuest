from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'field', 'start_date', 'end_date', 'exam_date', 'grade']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: 100%; padding: 10px;'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: 100%; padding: 10px;'}),
            'exam_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: 100%; padding: 10px;'}),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'exam_date': 'Exam Date',
        }

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('field', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Row(
                Column('exam_date', css_class='col-md-6'),
                Column('grade', css_class='col-md-6'),
            ),
        )
