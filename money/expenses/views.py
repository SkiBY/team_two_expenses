from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from . import models, forms
from django.db.models import Sum, FloatField


# def add_entry(request):
#     entry = models.Entry.object.all()
#     # return render(request, 'expenses/expenses.html', {'entry': entry, })
#     return render(request, '', {'entry': entry, })
#     pass
#
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
    if request.method == 'POST':
        form = forms.ChooseDate(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            date_money_min = clean_data
            date_money_max = clean_data
            entries = models.Entry.objects.filter(date_money__lt=date_money_max, date_money__gt=date_money_min)
            return render(request, 'expenses/filter.html', {'entries': entries})




        #
        #     new_entry = form.save(commit=False)
        #     new_entry.responsible_user_id = request.user
        #     new_entry.save()
        #     return redirect('expenses:entry_details', new_entry.id)
        # else:
        #     return render(request, 'expenses/filter.html', {'entries': entries})
        #     # return render(request, 'expenses/add_new_entry.html', {'form': form})
        #
    else:
        form = forms.ChooseDate()
        return render(request, 'expenses/filter.html', {'form': form})
        # return render(request, 'expenses/add_new_entry.html', {'form': form})









# def summa_expenses(request):
#     global summa_expenses
#     summa_expenses = sum(models.Entry.summa.filter(summa__type='expenses'))
#     if not summa_expenses:
#         raise Exception ('Not Expenses')
#
#     return render(request, 'expenses/income.html', {'expenses': summa_expenses,})
#
# def total(request):
#     total = summa_income - summa_expenses
#     return (request, 'expenses/total.html', {'expenses': total,})
#
#
#     pass


