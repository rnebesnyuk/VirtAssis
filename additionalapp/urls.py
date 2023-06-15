from django.urls import path
from . import views

app_name = 'additionalapp'

urlpatterns = [
    path('', views.main, name='main'),
]