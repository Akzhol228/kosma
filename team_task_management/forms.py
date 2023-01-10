from django import forms
from .models import Task,EmployeeDayRating


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['description', 'date', 'status', 'comment']
        labels = {
            'description':'Описание:',
            'date': 'Дата:',
            'status': 'Cтатус:',
            'comment': 'Комментарий:'
        }
        widgets = {'date': forms.HiddenInput()}


class EmployeeDayRatingForm(forms.ModelForm):

    class Meta:
        model = EmployeeDayRating
        fields = ['recomend_rating', 'date', 'comment']
        labels = {
            'recomend_rating': 'Рекомендовать рейтинг:',
            'date': 'Дата:',
            'comment': 'Комментарий:'
        }
        widgets = {'date': forms.HiddenInput()}
