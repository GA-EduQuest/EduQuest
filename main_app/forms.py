from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'field', 'start_date', 'end_date', 'exam_date', 'grade']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'exam_date': 'Exam Date',
        }
