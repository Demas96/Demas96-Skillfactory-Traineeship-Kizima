from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *

class PerevalAddTests(APITestCase):
    def test_perevaladd(self):
        us_test = Users.objects.create(username='test@test.ru', email='test@test.ru', first_name='test',
                                       last_name='test', patronymic='test',
                                       phone='test')
        for p in range(10):
            co_test = Coords.objects.create(latitude=0, longitude=0,
                                       height=0)
            pe_test = PerevalAdd.objects.create(
                coords=co_test,
                beauty_title='test',
                title='for_test3',
                other_titles='test',
                connect='test',
                add_time='2021-09-22 13:18:13.000 +0300',
                level_winter='test',
                level_summer='test',
                level_autumn='test',
                level_spring='test',
                user=us_test
            )
            Images.objects.create(pereval=pe_test, data='test', title='test')