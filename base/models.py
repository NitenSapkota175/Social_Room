from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from rx import create
from django.utils import timezone
# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True,blank=True)
    auth_token = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class Topic(models.Model):
    name =models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
     ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
        user = models.ForeignKey(User,on_delete = models.CASCADE)
        room = models.ForeignKey(Room,on_delete=models.CASCADE)
        body = models.TextField()
        updated = models.DateField(auto_now= True)
        created = models.DateField(auto_now_add=True)

        class Meta:
            ordering = ['-updated' ,'-created']

        def __str__(self):
            return self.body[0:50]

class Post(models.Model):
    #image 
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateField(auto_now=True)
    updated = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User,blank=True,related_name ='likes')

class comment(models.Model):
     author = models.ForeignKey(User,on_delete=models.CASCADE)
     comment = models.TextField ()
     post = models.ForeignKey(Post,on_delete=models.CASCADE)
     created = models.DateField(default=timezone.now)