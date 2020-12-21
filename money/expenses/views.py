from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .courses_money import rate
from . import models
from . import models, forms
from django.db.models import Sum, FloatField
#from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='login')
def add_entry(request):
    entry = models.Entry.objects.all()
    return render(request, 'expenses/operations.html', {'entry': entry, })


@login_required(login_url='login')
def all_income_expenses(request):
    entries = models.Entry.objects.all()
    return render(request, 'expenses/total.html', {'entries': entries})


@login_required(login_url='login')
def entry_details(request, entry_id: int):
    entry = models.Entry.objects.get(id=entry_id)
    if not entry:
        raise Exception('No such income/expenses')
    return render(request, 'expenses/total.html', {'entry': entry, })


@login_required(login_url='login')
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


@login_required(login_url='login')
def all_income(request):
    entries = models.Entry.objects.filter(type_inc_exp='income')
    if not all_income:
        raise Exception('No Income')
    income_rub = entries.filter(currency='RUB').aggregate(Sum('summa', output_field=FloatField()))
    income_usd = entries.filter(currency='USD').aggregate(Sum('summa'))
    income_euro = entries.filter(currency='EU').aggregate(Sum('summa'))
    income_byn = entries.filter(currency='BYN').aggregate(Sum('summa'))

    data = {'entries': entries,
            'income_rub': income_rub['summa__sum'] if income_rub['summa__sum'] is not None else 0,
            'income_usd': income_usd['summa__sum'] if income_usd['summa__sum'] is not None else 0,
            'income_euro': income_euro['summa__sum'] if income_euro['summa__sum'] is not None else 0,
            'income_byn': income_byn['summa__sum'] if income_byn['summa__sum'] is not None else 0}
    return render(request, 'expenses/income.html', context=data, )


@login_required(login_url='login')
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
            return render(request, 'expenses/filter.html', {'entries': entries, 'flag': flag,
                                                            'date_money_min': date_money_min,
                                                            'date_money_max': date_money_max,})
    else:
        form = forms.ChooseDate()
        return render(request, 'expenses/filter.html', {'form': form, 'flag': flag, })


@login_required(login_url='login')
def total_balance(request):
    courses = rate()
    total_exp = models.Entry.objects.filter(type_inc_exp='expenses')
    total_inc = models.Entry.objects.filter(type_inc_exp='income')
    balance = 0
    type_balance = 'BYN'

    form = forms.ChooseCurrency()
    if request.GET:
        tamp = request.GET['choose_courses']
    else:
        tamp = 'BYN'

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

    return render(request, 'expenses/total_balance.html', {'balance': round(balance / courses[tamp], 2),
                                                           'type_balance': type_balance, 'form': form, 'tamp': tamp})


@login_required(login_url='login')
def all_expenses(request):
    entries = models.Entry.objects.filter(type_inc_exp='expenses')
    if not all_income:
        raise Exception('No Expenses')
    expenses_rub = entries.filter(currency='RUB').aggregate(Sum('summa', output_field=FloatField()))
    expenses_usd = entries.filter(currency='USD').aggregate(Sum('summa'))
    expenses_euro = entries.filter(currency='EU').aggregate(Sum('summa'))
    expenses_byn = entries.filter(currency='BYN').aggregate(Sum('summa'))
    data = {'entries': entries,
            'expenses_rub': expenses_rub['summa__sum'] if expenses_rub['summa__sum'] is not None else 0,
            'expenses_usd': expenses_usd['summa__sum'] if expenses_usd['summa__sum'] is not None else 0,
            'expenses_euro': expenses_euro['summa__sum'] if expenses_euro['summa__sum'] is not None else 0,
            'expenses_byn': expenses_byn['summa__sum'] if expenses_byn['summa__sum'] is not None else 0}
    return render(request, 'expenses/expenses.html', context=data, )

def delete_entry(request, id):

    entry = models.Entry.objects.get(id=id)
    entry.delete()
    entries = models.Entry.objects.all()
    return render(request, 'expenses/total.html', {'entries': entries, })


def update_entry(request, id):
    entry = models.Entry.objects.get(id=id)
    form = forms.ExpensesForm(request.POST or None, instance=entry)


    if form.is_valid():
        form.save()
        return redirect('expenses:entry_details', entry.id)
    return render(request, 'expenses/add_new_entry.html', {'form': form})














