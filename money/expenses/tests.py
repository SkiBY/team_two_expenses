from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import Category, Entry
import datetime
from . import views


class EntryTest(TestCase):
    def setUp(self):
        self.сategory_1 = Category.objects.create(name='salary')
        self.сategory_2 = Category.objects.create(name='food')
        self.responsible_user_id = User.objects.create(username='P')
        # self.entry_1 = Entry.objects.create(summa=150, notes='salary', category=self.сategory_1, currency='BYN',
        #                                     responsible_user_id=self.responsible_user_id, date_money='2020-11-18',
        #                                     type_inc_exp='income')
        #
        # self.entry_2 = Entry.objects.create(summa=250, notes='salary', category=self.сategory_1, currency='EU',
        #                                     responsible_user_id=self.responsible_user_id, date_money='2020-11-20',
        #                                     type_inc_exp='income')
        for i in range(1,10):
            Entry.objects.create(summa=150*i, notes='salary_{}'.format(i), category=self.сategory_1, currency='BYN',
                                 responsible_user_id=self.responsible_user_id, date_money='2020-11-18',
                                 type_inc_exp='income')

        for i in range(1,10):
            Entry.objects.create(summa=97*i/3, notes='salary_{}'.format(i), category=self.сategory_1, currency='EU',
                                 responsible_user_id=self.responsible_user_id, date_money='2020-11-18',
                                 type_inc_exp='income')
        for i in range(1,90):
            Entry.objects.create(summa=97*i/3, notes='salary_{}'.format(i), category=self.сategory_1, currency='EU',
                                 responsible_user_id=self.responsible_user_id,
                                 date_money=datetime.date(2020,9,1)+datetime.timedelta(days=i-1),type_inc_exp='income')
        for i in range(20,40):
            Entry.objects.create(summa=36*i/7, notes='food_{}'.format(i), category=self.сategory_1, currency='BYN',
                                 responsible_user_id=self.responsible_user_id, date_money='2020-11-18',
                                 type_inc_exp='expenses')

    def test_calculate_income(self):
        print(views.calculate_income().get('income_byn'))
        self.assertEqual(views.calculate_income().get('income_byn'), 6750)










