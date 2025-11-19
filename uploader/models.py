from django.db import models

# Create your models here.
class SaveFile(models.Model):
    username = models.CharField(max_length=100)
    gameID = models.CharField(max_length=100)
    fileName = models.CharField(max_length=100)
    saveData = models.CharField()