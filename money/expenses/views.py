from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .courses_money import rate
from . import models
from . import models, forms
from django.db.models import Sum, FloatField


def add_entry(request):
    entry = models.Entry.objects.all()
    return render(request, 'expenses/operations.html', {'entry': entry, })


def all_income_expenses(request):
    entries = models.Entry.objects.all()
    return render(request, 'expenses/total.html', {'entries': entries, })


def entry_details(request, entry_id: int):
    entry = models.Entry.objects.get(id=entry_id)
    if not entry:
        raise Exception('No such income/expenses')
    return render(request, 'expenses/total.html', {'entry': entry, })


def add_new_entry(request):
    if request.method == 'POST':
        form = forms.ExpensesForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.responsible_user_id = request.user
            new_entry.save()
            return redirect('expenses:entry_details', new_entry.id)
        else:
            return render(request, 'expenses/add_new_entry.html', {'form': form})
    else:
        form = forms.ExpensesForm()
        return render(request, 'expenses/add_new_entry.html', {'form': form})


def all_income(request):
    entries = models.Entry.objects.filter(type_inc_exp='income')
    if not all_income:
        raise Exception('No Income')
    income_rub = entries.filter(currency='RUB').aggregate(Sum('summa', output_field=FloatField()))
    income_usd = entries.filter(currency='USD').aggregate(Sum('summa'))
    income_euro = entries.filter(currency='EURO').aggregate(Sum('summa'))
    income_byn = entries.filter(currency='BYN').aggregate(Sum('summa'))

    data = {'entries': entries,
            'income_rub':income_rub,
            'income_usd':income_usd,
            'income_euro':income_euro,
            'income_byn':income_byn}
    return render(request, 'expenses/income.html', context=data, )


def choose_date(request):
    flag = False
    if request.method == 'POST':
        form = forms.ChooseDate(request.POST)
        if form.is_valid():
            flag = True
            clean_data = form.cleaned_data
            date_money_min = clean_data['date_money_min']
            date_money_max = clean_data['date_money_max']
            entries = models.Entry.objects.filter(date_money__lt=date_money_max, date_money__gt=date_money_min)
            return render(request, 'expenses/filter.html', {'entries': entries, 'flag': flag})
    else:
        form = forms.ChooseDate()
        return render(request, 'expenses/filter.html', {'form': form, 'flag': flag})


def total_balance(request):
    courses = rate()
    total_exp = models.Entry.objects.filter(type_inc_exp='expenses')
    total_inc = models.Entry.objects.filter(type_inc_exp='income')
    balance = 0
    type_balance = 'BYN'

    for i in total_inc:
        if type_balance == i.currency:
            balance += i.summa
        elif i.currency == 'RUB':
            balance += i.summa * courses['RUB']
        elif i.currency == 'USD':
            balance += i.summa * courses['USD']
        elif i.currency == 'EU':
            balance += i.summa * courses['EU']

    for i in total_exp:
        if type_balance == i.currency:
            balance -= i.summa
        elif i.currency == 'RUB':
            balance -= i.summa * courses['RUB']
        elif i.currency == 'USD':
            balance -= i.summa * courses['USD']
        elif i.currency == 'EU':
            balance -= i.summa * courses['EU']

    return render(request, 'expenses/total_balance.html', {'balance': balance, 'type_balance': type_balance})


