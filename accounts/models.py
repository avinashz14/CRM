from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ManyToManyField

from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=CASCADE)
    name = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
class Tag(models.Model):
    tag = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.tag


class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
    )
    name =  models.CharField(max_length=250, null=True)
    price =  models.FloatField(null=True)
    category =  models.CharField(max_length=250, null=True, choices=CATEGORY)
    description =  models.CharField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tag = ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out of delivery', 'Out of delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey(Customer, null = True, on_delete=SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete=SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name
