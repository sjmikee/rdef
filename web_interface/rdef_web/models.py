from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class urls(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=150, null=True,  blank=True)
    user = models.CharField(max_length=30, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    protocol = models.CharField(max_length=30, null=True, blank=True)


class whitelist(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=150, null=True, blank=True)


class blacklist(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=150, null=True, blank=True)
