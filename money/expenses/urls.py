from django.contrib import admin
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # path('', views.add_entry, name='entry'),
    path('', views.all_income_expenses, name='all_income_expenses'),
    path('entry/<int:entry_id>', views.entry_details, name='entry_details'),
    path('new_entry/', views.add_new_entry, name='add_new_entry'),
    path('income/', views.all_income, name='all_income'),
    path('choose/', views.choose_date, name='choose_date'),


    path('operations/', views.add_entry, name='entry'),
    path('total_balance/', views.total_balance, name='total_balance'),

    ]
