from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .courses_money import rate
from . import models



def add_entry(request):
    entry = models.Entry.objects.all()
    # return render(request, 'expenses/expenses.html', {'entry': entry, })
    return render(request, 'expenses/operations.html', {'entry': entry, })

def summa_income(request):

    summa_income = sum(models.Entry.objects.filter(summa__type='income'))
    if not summa_income:
        raise Exception('No Income')

    return render(request, 'expenses/income.html', {'expenses': summa_income, })

def summa_expenses(request):
    summa_expenses = sum(models.Entry.summa.filter(summa__type='expenses'))
    if not summa_expenses:
        raise Exception ('Not Expenses')

    return render(request, 'expenses/income.html', {'expeses': summa_expenses,})

def total(request):
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

    return render(request, 'expenses/total.html', {'balance': balance, 'type_balance': type_balance} )



