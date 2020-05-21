from django.contrib import admin
from django.urls import path
from baza import views
urlpatterns = [
    path('', views.index),
    path('add',views.add),
    path('search',views.search),
    path('delete',views.delete),
    path('edit',views.edit),
]
