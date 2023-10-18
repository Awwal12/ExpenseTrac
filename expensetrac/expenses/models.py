from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    date = models.DateTimeField()
    description = models.TextField() 
    amount= models.FloatField()
    category = models.CharField(max_length=256)
    owner= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}'

    class Meta:
        ordering:['-date']

class Category(models.Model):
    name= models.CharField(max_length=256)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    