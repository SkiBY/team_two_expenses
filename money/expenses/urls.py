from django.contrib import admin
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # path('', views.add_entry, name='entry'),
    path('', views.all_income_expenses, name='all_income_expenses'),
    path('entry/<int:id>', views.entry_details, name='entry_details'),
    path('new_entry/', views.add_new_entry, name='add_new_entry'),
    path('income/', views.all_income, name='all_income'),
    path('choose/', views.choose_date, name='choose_date'),
    path('expenses/', views.all_expenses, name='all_expenses'),

    path('operations/', views.add_entry, name='entry'),
    path('total_balance/', views.total_balance, name='total_balance'),
    path('delete/<int:id>', views.delete_entry, name='delete'),

    path('update/<int:id>', views.update_entry, name='update_entry'),
    # path('update/', views.update_entry, name='entry_details'),

    ]
