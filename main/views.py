import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import *
from rest_framework.views import APIView

from .serializers import PerevalSerializer


def submitData(request):
    try:
        json_body = json.loads(request.body)
        user = json_body['user']
        coords = json_body['coords']
        level = json_body['level']
        images = json_body['images']
        # serialiser = PerevalSerializer(data=request.data)
        # serialiser.is_valid(raise_exception=True)
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
        pe = PerevalAdd.objects.create(coords=co, beauty_title=json_body['beauty_title'],
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
        return data

    except KeyError as exc:
        data = {
            'status': '400',
            'message': f'Не хватает полей {exc}',
            'id': 'null'
        }
        return data

    except Exception as exc:
        data = {
            'status': '500',
            'message': f'{exc}',
            'id': 'null'
        }
        return data


class PerevalAPIView(APIView):

    def post(self, request):
        data = submitData(request)
        return JsonResponse(data, status=data['status'])

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            data = PerevalSerializer(PerevalAdd.objects.get(pk=pk)).data
        except Exception as exc:
            data = {
                'message': f'Нет записи с id = {pk} {exc}'
            }
        return JsonResponse(data)

    def get_object(self, pk):
        return PerevalAdd.objects.get(pk=pk)

    def patch(self, request, pk):
        if PerevalAdd.objects.filter(pk=pk).values('status')[0]['status'] == 'NEW':
            try:
                obj = self.get_object(pk)
                serializer = PerevalSerializer(obj, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data = {
                        'state': 1,
                        'message': 'Данные обновлены'
                    }
                    return JsonResponse(data)
                return JsonResponse(code=400, data="wrong parameters")

            except Exception as exc:
                data = {
                    'state': 0,
                    'message': f'Не удалось обновить запись: {exc}'
                }
                return JsonResponse(data)
        else:
            data = {
                'state': 0,
                'message': f"Не удалось обновить запись: статус записи "
                           f"{PerevalAdd.objects.filter(pk=pk).values('status')[0]['status']}"
            }
            return JsonResponse(data)


class EmailAPIView(APIView):
    def get(self, *args, **kwargs):
        email = kwargs.get('email', None)
        if PerevalAdd.objects.filter(user__email=email):
            data = PerevalSerializer(PerevalAdd.objects.filter(user__email=email), many=True).data
        else:
            data = {
                'message': f'Нет записей от email = {email}'
            }
        return JsonResponse(data, safe=False)
