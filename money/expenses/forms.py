from django import forms
from . import models


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = '__all__'
        # exclude = ['']


class ChooseDate(forms.Form):
    date_money_min = forms.DateField()
    date_money_max = forms.DateField()


class ChooseCurrency(forms.Form):
    choose_courses = forms.ChoiceField(choices=models.CURRENCY)



