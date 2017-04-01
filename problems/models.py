from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Problems(models.Model):
    code = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    type = models.CharField(max_length=255,null=True,blank=True)
    contest = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True)
    pgroup = models.CharField(max_length=255,null=True,blank=True)
    statement = models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)
    input = models.TextField(null=True,blank=True)
    output = models.TextField(null=True,blank=True)
    timelimit = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    score = models.IntegerField(null=True,blank=True)
    language = models.CharField(max_length=255,null=True,blank=True)
    options = models.CharField(max_length=255,null=True,blank=True)
    displayio = models.IntegerField(null=True,blank=True)
    solved = models.IntegerField(null=True,blank=True,default=0)
    total = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.name

class Runs(models.Model):
    problem = models.ForeignKey(Problems,on_delete=models.CASCADE)
    tid = models.IntegerField(null=True,blank=True)
    language = models.CharField(max_length=255,null=True,blank=True)
    time = models.CharField(max_length=255,null=True,blank=True)
    result = models.CharField(max_length=255,null=True,blank=True)
    access = models.CharField(max_length=255,null=True,blank=True)
    submittime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #submittime = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.id)

class Subs_code(models.Model):
    run = models.ForeignKey(Runs,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True,blank=True)
    code = models.TextField(null=True,blank=True)
    error = models.TextField(null=True,blank=True)
    output = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.id)