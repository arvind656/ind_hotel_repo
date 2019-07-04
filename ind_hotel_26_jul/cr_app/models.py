# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
# import django.urls to set absolute URL
from django.urls import reverse

from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User_t(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    city_name = models.CharField(max_length=200)
    rooms = models.CharField(max_length=200)
    
    # It's always fine knowing when it is created
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        unique_together = (('hotel_name', 'city_name'),)

    # Inspect Book object via name
    def __str__(self):
        return self.hotel_name

    # Inspect absolute Book object's URL
    def get_absolute_url(self):
        return reverse('hotel_edit', kwargs={'pk': self.pk})

class Pricing(models.Model):
    starting_price = models.IntegerField()
    business_suite_price = models.IntegerField()
    presedential_suite_price = models.IntegerField()
    
    hotel = models.ForeignKey(Hotel,primary_key=True, on_delete=models.CASCADE)
    objects = models.Manager()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    objects = models.Manager()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if (created):
        Profile.objects.create(user=instance)
        #profile.objects.create(user=instance)
    instance.profile.save()
