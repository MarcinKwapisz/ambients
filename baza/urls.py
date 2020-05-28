from django.contrib import admin
from django.urls import path
from baza import views
urlpatterns = [
    path('', views.index),
    path('add',views.add),
    path('search',views.search),
    path('delete',views.delete),
    path('edit',views.edit),
    path('user',views.user),
    path('admini',views.admini),
    path('login',views.login),
    path('register',views.register),
    path('logout',views.logout),
]
