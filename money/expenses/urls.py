from django.contrib import admin
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.add_entry, name='entry'),


    ]
