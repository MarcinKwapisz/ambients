from django.shortcuts import render, redirect
from django.contrib.auth import models as mod, authenticate,login as authlog,logout as authlogout
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from . import models
import urllib.request
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required

# Create your views here.

def getName(link, ret=0):
    soup = BeautifulSoup(urllib.request.urlopen(link), features="html.parser")
    name = soup.title.string
    name = name.encode('ascii', 'ignore').decode('ascii')
    if len(name)<10 and ret==0:
        getName(link,1)
    if len(name)<10 and ret==1:
        return name
    else:
        return name[0:-10]

def encode(value):
    return value.encode('ascii', 'ignore').decode('ascii')

def add_to_base(link, opis, kategorie, dodal):

    models.Ambients.objects.create(link=encode(link), linkName=getName(link), opis=encode(opis),
                                   kategorie=encode(kategorie), dodal=dodal, glosy=0)


def getlink(link):
    soup = BeautifulSoup(urllib.request.urlopen(link))
    name = soup.getSiteName

def index(request):
    form = models.Ambients.objects.values_list().order_by('-glosy')
    return render(request, 'index.html', {'form':form})

@login_required
def add(request):
    if request.method == "GET":
        return render(request, 'add.html')
    else:
        li = request.POST
        if len(models.Ambients.objects.filter(link__contains=li['link'])) == 0:
            add_to_base(link=li['link'],opis=li['opis'],kategorie=li['kategorie'],dodal=request.user.id)
            messages.success(request, "Dodane")
            return redirect('/')
        else:
            messages.warning(request, "Coś poszło nie tak")
            return redirect('/add')


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

@login_required
def delete(request):
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
                    messages.success(request, "Usunięto!")
                else:
                    messages.warning(request, "Coś poszło nie tak :(")
                    pass
        return redirect('/')

@login_required
def edit(request):
    if request.method == "GET":
        id = request.GET.get('id', '')
        if id == '':
            messages.warning(request, "Nie kombinuj")
            return redirect('/')
        else:
            obj = models.Ambients.objects.get(id=id)
            if obj.dodal == request.user.id or request.user.is_superuser:
                return render(request, 'edit.html', {'obj': obj})
            else:
                messages.warning(request, "Nie kombinuj")
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
        messages.success(request, "Zedytowane")
        return redirect('/user')

@login_required
def user(request):
    user = request.user.id
    form = models.Ambients.objects.all().filter(dodal=user)
    return render(request, 'user.html', {'form': form}, )


def admini(request):
    if request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        messages.warning(request, "You shall not pass!")
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
            messages.success(request, "Zalogowano pomyślnie")
            return redirect('/')
        else:
            messages.warning(request, 'Zła nazwa lub hasło')
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
            messages.success(request, "Utworzono konto")
            return redirect('/login')
        else:
            messages.warning(request, "Jest już taki użytkownik")
            return redirect('/register')

def logout(request):
    if request.user.is_authenticated:
        authlogout(request)
        messages.success(request, "Wylogowano pomyślnie")
        return redirect('/')
    else:
        messages.warning(request, "Nie jesteś zalogowany")
        return redirect('/')


def voteup(request):
    post = request.POST['id']
    user = request.user.id
    if not models.Votes.objects.filter(ambient_id=post, user_id=user):
        models.Votes.objects.create(ambient_id=post, user_id=user)
        obj = models.Ambients.objects.get(id=post)
        obj.glosy +=1
        obj.save()
    return HttpResponse("Success")
