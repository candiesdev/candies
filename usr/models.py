from django.db import models

# Create your models here.

class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    url=models.CharField(max_length=200)

def __str__(self):
    return self.title