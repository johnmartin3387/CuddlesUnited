from __future__ import unicode_literals

from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True, default="")

    pet_name = models.CharField(max_length=255, blank=True, null=True)

    type = models.CharField(max_length=255, blank=True, null=True) # dog or cat
    size = models.CharField(max_length=255, blank=True, null=True)
    breed = models.CharField(max_length=255, blank=True, null=True)
    mixed = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True, default="")
    color_sec = models.CharField(max_length=255, blank=True, null=True, default="")
    sex = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField()
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    microchip = models.BooleanField(default=False)
    collor = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True, default="")
    verified_email = models.IntegerField(default=0, null=True, blank=True)
    pet_image = models.CharField(max_length=255, blank=True, null=True)
    pricing = models.IntegerField(default=0, null=True, blank=True)
    stripe_uid = models.CharField(max_length=255, blank=True, null=True, default="")
    
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Client'


class Pet(models.Model):
    client = models.ForeignKey('client', blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    # created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Pet'

class Post(models.Model):
    client = models.ForeignKey('client', blank=True, null=True)
    path_key = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Post'

class Comment(models.Model):
    post = models.ForeignKey('post', blank=True, null=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comment'

