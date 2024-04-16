from django.contrib import admin
from django.urls import path, include
from .views import entry_list, entry_detail

urlpatterns = [
    path('entries/', entry_list, name='entry_list'),
    path('entries/<int:pk>', entry_detail, name='entry_detail')
]
