from django.http import JsonResponse
from rest_framework.views import APIView

from .models import *
from rest_framework import generics
from .serializers import PerevalSerializer, PerevalDetailSerializer





class PerevalAPIView(APIView):

    def post(self, request):
        pereval = PerevalSerializer(data=request.data)
        try:
            if pereval.is_valid(raise_exception=True):
                data = pereval.save()
                return JsonResponse(data, status=200, safe=False)
        except Exception as exc:
            data = {
                'status': '400',
                'message': f'Не хватает полей {exc}',
                'id': 'null'
            }
        return JsonResponse(data, status=400, safe=False)

    def get(self, request, *args, **kwargs):
        email = request.GET.get('user__email', None)
        if PerevalAdd.objects.filter(user__email=email):
            data = PerevalDetailSerializer(PerevalAdd.objects.filter(user__email=email), many=True).data
        else:
            data = {
                'message': f'Нет записей от email = {email}'
            }
        return JsonResponse(data, safe=False)


class PerevalListAPIView(generics.ListAPIView):
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            data = PerevalDetailSerializer(PerevalAdd.objects.get(pk=pk)).data
        except Exception as exc:
            data = {
                'message': f'Нет записи с id = {pk}'
            }
        return JsonResponse(data)

    def get_object(self, pk):
        return PerevalAdd.objects.get(pk=pk)

    def patch(self, request, pk):
        try:
            if PerevalAdd.objects.filter(pk=pk).values('status')[0]['status'] == 'NEW':
                obj = self.get_object(pk)
                serializer = PerevalSerializer(obj, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data = {
                        'state': 1,
                        'message': 'Данные обновлены'
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'state': 0,
                    'message': f"Не удалось обновить запись: статус записи "
                               f"{PerevalAdd.objects.filter(pk=pk).values('status')[0]['status']}"
                }
                return JsonResponse(data)

        except Exception as exc:
            data = {
                'state': 0,
                'message': f'Не удалось обновить запись: {exc}'
            }
            return JsonResponse(data)

