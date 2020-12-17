from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# INCOME = [
#     ('salary','Salary'),
#     ('gift','Gift'),
#     ('lottery','Lottery'),
# ]
#
# EXPENSES = [
#     ('food','Food')
# ]

CURRENCY = [
    ('dollar','Dollar'),
    ('euro','Euro'),
    ('rub', 'Rub')
]
TYPE = [
    ('income', 'Income'),
    ('expenses', 'Expenses'),

]

class Total(models.Model):
    summa_income = models.FloatField(verbose_name='summa_income')
    summa_expenses = models.FloatField(verbose_name='summa_expenses')
    total = models.FloatField(verbose_name='total')

    def __str__(self):
        return self.total

class Source_types(models.Model):
    type = models.CharField(max_length=100, verbose_name='Type', choices=TYPE, default='expenses')
    responsible_user_id = models.ForeignKey(User, verbose_name='Responsible', related_name='car_to_user', null=True,
                                            on_delete=models.SET_NULL)

    def __str__(self):
        return self.type


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Entry(models.Model):
    summa = models.FloatField()#прописать чтобы + числа
    сategory = models.ForeignKey(Category, related_name='entry_to_category', verbose_name='category', on_delete=models.RESTRICT)
    currency = models.CharField(max_length=100, verbose_name='Currency', choices=CURRENCY, default='rub')
    source = models.ForeignKey(Source_types, related_name='entry_to_source', verbose_name='source', on_delete=models.RESTRICT)
    date_money = models.DateField(verbose_name='date_money')
    date_entry = models.DateTimeField(verbose_name='date_entry', auto_now_add=True)


    def __str__(self):
        return '{}, {}'.format(self.summa, self.date_money)
