from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out of delivery', 'Out of delivery'),
        ('Delivered','Delivered'),
    )
    #customer =
    #product =
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, null=True, choices=STATUS)
