from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('submitData/<int:pk>/', PerevalListAPIView.as_view()),
    path('submitData/', PerevalAPIView.as_view()),
    path('submitData/user__email=<str:email>', PerevalEmailAPIView.as_view()),
]
