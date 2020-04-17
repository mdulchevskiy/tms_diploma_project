from django.db import models
from django.db.models import SET_NULL


class SweetType(models.Model):
    sweet_type = models.CharField(max_length=255, default=None)

    def __str__(self):
        return f'{self.sweet_type}'


class Sweet(models.Model):
    sweet = models.CharField(max_length=255, default=None)
    price = models.FloatField()
    type = models.ForeignKey('SweetType', null=True, on_delete=SET_NULL, related_name='sweets')

    def __str__(self):
        return f'{self.pk}: {self.type}, {self.sweet}'


class User(models.Model):
    username = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255, default=None)
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=17, default=None)
    address = models.CharField(max_length=255, default=None)
    login = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pk}: {self.username}'


class Basket(models.Model):
    sweet_id = models.IntegerField()
    sweet_type = models.CharField(max_length=255, default=None)
    sweet = models.CharField(max_length=255, default=None)
    price = models.FloatField()
    amount = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return f'{self.pk}: {self.sweet}'


class Order(models.Model):
    user_type = models.CharField(max_length=255, default='Guest')
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=17, default=None)
    address = models.CharField(max_length=255, default=None)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    comment = models.CharField(max_length=510, null=True)
    order_info = models.CharField(max_length=2040)
    user = models.ForeignKey('User', null=True, on_delete=SET_NULL, related_name='orders')

    def __str__(self):
        return f'Order {self.pk}'
