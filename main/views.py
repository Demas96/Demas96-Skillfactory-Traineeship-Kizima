import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import *
from rest_framework.views import APIView


class PerevalAPIView(APIView):
    def post(self, request):
        try:
            json_body = json.loads(request.body)
            user = json_body['user']
            coords = json_body['coords']
            level = json_body['level']
            images = json_body['images']
            if Users.objects.filter(email=user['email']).exists():
                Users.objects.filter(email=user['email']).update(firstname=user['name'],
                                           lastname=user['fam'], patronymic=user['otc'],
                                           phone=user['phone'])
                uss = Users.objects.get(email=user['email'])
            else:
                us = User.objects.create(username=user['email'])
                uss = Users.objects.create(user=us, email=user['email'], firstname=user['name'],
                                           lastname=user['fam'], patronymic=user['otc'],
                                           phone=user['phone'])

            co = Coords.objects.create(latitude=coords['latitude'], longitude=coords['longitude'],
                                       height=coords['height'])
            pe = PerevalAdd.objects.create(coords=co, beautyTitle=json_body['beauty_title'],
                                           title=json_body['title'], other_titles=json_body['other_titles'],
                                           connect=json_body['connect'], add_time=json_body['add_time'],
                                           level_winter=level['winter'], level_summer=level['summer'],
                                           level_autumn=level['autumn'], level_spring=level['spring'],
                                           user=uss)

            for obj in images:
                Images.objects.create(pereval=pe, img=obj['data'], title=obj['title'])
            data = {
                'status': '200',
                'message': 'null',
                'id': f"{pe.id}"
            }
            return JsonResponse(data, status=200)

        except Exception as exs:
            data = {
                'status': '500',
                'message': f'{exs}',
                'id': 'null'
            }
            return JsonResponse(data, status=500)

        except KeyError as exs:
            data = {
                'status': '400',
                'message': 'Не хватает полей',
                'id': 'null'
            }
            return JsonResponse(data, status=400)
