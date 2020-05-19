from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import models
import urllib.request
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
    form = models.Ambients.objects.values_list()
    return render(request, 'index.html', {'form':form})

def add(request):
    if request.method == "GET":
        return render(request, 'add.html')
    else:
        li = request.POST
        if len(models.Ambients.objects.filter(link__contains=li['link'])) == 0:
            soup = BeautifulSoup(urllib.request.urlopen(li['link']))
            models.Ambients.objects.create(link=li['link'],linkName=soup.title.string,opis=li['opis'],kategorie=li['kategorie'])
            return HttpResponse('<meta http-equiv="Refresh" content="2"; url="/" />Dodano')
        else:
            return HttpResponse('<meta http-equiv="Refresh" content="2"; url="/" />Jest już taki ambient')

def search(request):
    name = request.POST['search']
    queries = models.Ambients.objects.filter(kategorie__contains=name)
    print(queries)