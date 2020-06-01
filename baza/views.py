from django.shortcuts import render, redirect
from django.contrib.auth import models as mod, authenticate,login as authlog,logout as authlogout
from django.http import HttpResponse, HttpRequest
from . import models
import urllib.request
from bs4 import BeautifulSoup
import re

# Create your views here.

def getName(link, ret=0):
    soup = BeautifulSoup(urllib.request.urlopen(link))
    name = soup.title.string
    name = name.encode('ascii', 'ignore').decode('ascii')
    if len(name)<10 and ret==0:
        getName(link,1)
    if len(name)<10 and ret==1:
        return name
    else:
        return name[0:-10]

def getlink(link):
    soup = BeautifulSoup(urllib.request.urlopen(link))
    name = soup.getSiteName

def index(request):
    form = models.Ambients.objects.values_list()
    return render(request, 'index.html', {'form':form}, )

def add(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'add.html')
        else:
            li = request.POST
            if len(models.Ambients.objects.filter(link__contains=li['link'])) == 0:
                models.Ambients.objects.create(link=li['link'],linkName=getName(li['link']),opis=li['opis'],kategorie=li['kategorie'],dodal=request.user.id)
                return redirect('/')
            else:
                return HttpResponse('<meta http-equiv="Refresh" content="1"; url="/" />Jest już taki ambient')
    else:
        return redirect('/login')

def search(request):
    name = request.POST['search']
    type = request.POST['type']
    if type == 'Nazwa':
        queries = models.Ambients.objects.all().filter(linkName__icontains=name)
    elif type == "Opis":
        queries = models.Ambients.objects.all().filter(opis__icontains=name)
    else:
        queries = models.Ambients.objects.all().filter(kategorie__icontains=name)
    return render(request,'search.html',{'queries': queries})

def delete(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user.id
            form = models.Ambients.objects.all().filter(dodal=user)
            return render(request, 'delete.html', {'form': form})
        else:
            lista = request.POST
            for i in lista:
                if i == "csrfmiddlewaretoken":
                    pass
                else:
                    mod = models.Ambients.objects.get(id=i)
                    if mod.dodal == request.user.id or request.user.is_superuser:
                        mod.delete()
                    else:
                        pass
            return redirect('/')
    else:
        return redirect('/login')

def edit(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            id = request.GET.get('id', '')
            if id == '':
                return redirect('/')
            else:
                obj = models.Ambients.objects.get(id=id)
                if obj.dodal == request.user.id or request.user.is_superuser:
                    return render(request, 'edit.html', {'obj': obj})
                else:
                    return redirect('/')
        else:
            lista = request.POST
            obj = models.Ambients.objects.get(id=lista['id'])
            obj.opis=lista['opis']
            obj.kategorie=lista['kategorie']
            l = getName(lista['link'])
            obj.linkName=l
            obj.link=lista['link']
            obj.save()
            return redirect('/user')
    else:
        return redirect('/login')

def user(request):
    if request.user.is_authenticated:
        user = request.user.id
        form = models.Ambients.objects.all().filter(dodal=user)
        return render(request, 'user.html', {'form': form}, )
    else:
        return redirect('login')

def admini(request):
    if request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        return redirect('/')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/user')
        else:
            return render(request, 'login.html')
    else:
        lista = request.POST
        if lista.getlist('remember'):
            log = authenticate(username=lista['name'], password=lista['password'])
        else:
            log = authenticate(username=lista['name'], password=lista['password'])
            request.session.set_expiry(0)
        if log is not None:
            authlog(request, log)
            return redirect('/')
        else:
            return redirect('/login')

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("/user")
        else:
            return render(request, 'register.html')
    else:
        lista = request.POST
        if not mod.User.objects.filter(username=lista['name']) or not mod.User.objects.filter(email=lista['email']):
            user = mod.User.objects.create_user(lista['name'], lista['email'], lista['password'])
            user.save()
            return redirect('/login')
        else:

            return redirect('/register')

def logout(request):
    if request.user.is_authenticated:
        authlogout(request)
        return redirect('/')
    else:
        return redirect('/')