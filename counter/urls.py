from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
        path('', views.index, name='index'),
        path('frequency/', views.frequency, name='frequency'),
        path('results/', views.results, name='results')
]
