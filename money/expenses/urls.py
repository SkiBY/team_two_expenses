from django.contrib import admin
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('operations/', views.add_entry, name='entry'),
    path('', views.total, name='total'),



    ]
