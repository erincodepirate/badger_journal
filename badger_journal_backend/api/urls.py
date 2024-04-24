from django.urls import path, include
from .views import register_user, entry_list, entry_detail

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('entries/', entry_list, name='entry_list'),
    path('entries/<int:pk>', entry_detail, name='entry_detail')
]
