from __future__ import unicode_literals

import uuid

from django.db import models


# Create your models
class user(models.Model):
    name  = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, null=False, blank=False)
    email = models.CharField(max_length=255, null=False, blank=False)
    contact = models.IntegerField(default=0)
    password = models.CharField(max_length=255, null=False,blank=False)
    short_bio = models.CharField(max_length=255, null=False,blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class AccessToken(models.Model):
    users_id = models.ForeignKey(user)
    access_token= models.CharField(max_length=255,null=0,blank=False)
    created_on= models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.access_token = uuid.uuid4()

class Movie(models.Model):

    name=models.CharField(max_length=255, null=False, blank=False)
    duration_in_minutes = models.IntegerField(default=0)
    release_date = models.DateField()
    overall_rating = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    censor_board_rating = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    poster_picture_url = models.CharField(max_length=255, null=False, blank=False)
    user_id = models.ForeignKey(user)





class Review(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(user)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    review = models.CharField(max_length=3000)


class Genre(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class MovieGenre(models.Model):
    genre_id = models.ForeignKey(Genre)
    movie_id = models.ForeignKey(Movie)
