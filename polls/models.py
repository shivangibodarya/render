from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    std = models.CharField(max_length=200)
