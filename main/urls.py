from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/', PerevalAPIView.as_view()),
]
