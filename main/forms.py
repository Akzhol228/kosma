from django import forms

from .models import CallBack


class CallBackForm(forms.ModelForm):

    class Meta:
        model = CallBack
        fields = ['phone_number', 'last_name', 'first_name']
