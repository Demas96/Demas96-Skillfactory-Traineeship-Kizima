from django.urls import path, include
from .views import *

urlpatterns = [
    path('submitData/', PerevalAPIView.as_view()),
    path('submitData/<int:pk>/', PerevalAPIView.as_view()),
]
