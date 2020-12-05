from django.urls import path, include
from . import views
from . import CountryDeath

urlpatterns = [
    path('', views.home, name='home'),
]