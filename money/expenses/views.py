from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from . import models, forms

def add_entry(request):
    entry = models.Entry.object.all()
    # return render(request, 'expenses/expenses.html', {'entry': entry, })
    return render(request, '', {'entry': entry, })



    pass

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

    pass


