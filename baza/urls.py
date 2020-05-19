from django.contrib import admin
from django.urls import path
from baza import views
urlpatterns = [
    path('', views.index),
    path('add',views.add),
    path('test',views.test),
]
