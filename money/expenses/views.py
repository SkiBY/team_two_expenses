from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from . import models, forms

def add_entry(request):

    pass

def summa_income (request):

    pass


def summa_expenses(request):
    summa_expenses = sum(models.Entry.summa.filter(summa__type='expenses'))
    if not summa_expenses:
        raise Exception ('Not Expenses')

    return render(request, 'expenses/income.html', {'expeses': summa_expenses,})

def total(request):

    pass


