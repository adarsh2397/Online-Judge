from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class UserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL    )
    profile_update = models.BooleanField(default=False)
    totalscore = models.IntegerField(default=0)
    college = models.CharField(max_length=255,null=True,blank=True)
    profileimage = models.FileField(null=True,blank=True)
    dateofbirth = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    joinDate = models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.user.username