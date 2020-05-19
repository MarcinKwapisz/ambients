from django.db import models

# Create your models here.



class Ambients(models.Model):
    link = models.TextField(unique=True)
    linkName = models.TextField()
    opis = models.TextField()
    kategorie = models.TextField()
