from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request, username=clean_data['login'], password=clean_data['password'])
            if not user:
                return HttpResponse('Bac Нету')
            if user.is_active:
                login(request, user)
                return redirect('expenses: all_income_expenses')
            else:
                return HttpResponse('Your user is inactive.')
        return render(request, 'login.html', {'form': form})
    else:
        form = forms.LoginForm()

        return render(request, 'login.html', {'form': form})
