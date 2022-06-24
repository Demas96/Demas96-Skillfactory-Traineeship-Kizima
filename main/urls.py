from django.urls import path, include
from .views import submitData

urlpatterns = [
    path('submitData', submitData),
]