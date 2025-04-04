from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications'),
    path('json/', views.notifications_json, name='notifications_json'),
]
