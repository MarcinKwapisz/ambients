from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Ambients(models.Model):
    link = models.TextField(unique=True)
    linkName = models.TextField()
    opis = models.TextField()
    kategorie = models.TextField()
    glosy = models.IntegerField()
    dodal = models.IntegerField()