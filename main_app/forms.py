from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Subject
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Your password can't be too similar to your other personal information, must contain at least 8 characters, and can't be entirely numeric."
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')



class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'field', 'start_date', 'end_date', 'exam_date', 'grade']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: 100%; padding: 10px;'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: 100%; padding: 10px;'}),
            'exam_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width: 100%; padding: 10px;'}),
            'grade': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%; padding: 10px; display: none;'}),
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
