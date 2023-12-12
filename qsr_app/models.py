from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
class cart(models.Model):
    username=models.CharField(max_length=20)
    product=models.CharField(max_length=20)
    prodimg=models.ImageField()
    quantity=models.IntegerField()
    price=models.IntegerField()
    total=models.IntegerField()
'''
class product(models.Model):
    CAT=((1,'Milk products'),(2,'confectionery'),(3,'Snacks'))
    name=models.CharField(max_length=50,verbose_name='Product name')
    price=models.FloatField()
    pdetails=models.TextField(verbose_name='Details')
    cat=models.IntegerField(verbose_name='Category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='Available')
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    ord_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class custadd(models.Model):
    ord_id=models.ForeignKey(Order,on_delete=models.CASCADE,db_column='ord_id')
    name=models.CharField(max_length=50)
    mobile=models.BigIntegerField()
    add1=models.TextField()
    add2=models.TextField()
    zip=models.IntegerField()
