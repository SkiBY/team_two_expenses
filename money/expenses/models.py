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
    ('USD', 'USD'),
    ('EU', 'EU'),
    ('RUB', 'RUB'),
    ('BYN', 'BYN'),
]
TYPE = [
    ('income', 'Income'),
    ('expenses', 'Expenses'),

]


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Entry(models.Model):
    summa = models.FloatField()#прописать чтобы + числа
    сategory = models.ForeignKey(Category, related_name='entry_to_category', verbose_name='category', on_delete=models.RESTRICT)
    currency = models.CharField(max_length=100, verbose_name='Currency', choices=CURRENCY, default='RUB')
    # source = models.ForeignKey(Source_types, related_name='entry_to_source', verbose_name='source', on_delete=models.RESTRICT)
    type_inc_exp = models.CharField(max_length=100, verbose_name='Type', choices=TYPE, default='expenses')
    responsible_user_id = models.ForeignKey(User, verbose_name='Responsible', related_name='car_to_user', null=True,
                                            on_delete=models.SET_NULL)
    date_money = models.DateField(verbose_name='date_money')
    date_entry = models.DateTimeField(verbose_name='date_entry', auto_now_add=True)

    def __str__(self):
        if self.type_inc_exp == 'income':
            return f'Зачисление {self.summa} {self.currency}. DATA {self.date_money}'
        else:
            return f'Оплата {self.summa} {self.currency}. DATA {self.date_money}'

