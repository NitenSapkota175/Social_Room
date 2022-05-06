from tkinter import CASCADE
from django.db import models
from django.urls.base import reverse
from rx import create
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length = 100,null=True)
    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []





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
            ordering = ['updated' ,'created']

        def __str__(self):
            return self.body[0:50]

class Post(models.Model):
    Post_image = models.ImageField(blank=True,null=True) 
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateField(auto_now=True)
    updated = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User,blank=True,related_name ='likes')
    dislikes = models.ManyToManyField(User,blank=True,related_name ='dislikes')
    title_tags = models.CharField(max_length=100)
    
    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.body[0:10] 

    def get_absolute_url(self):
        return reverse('Home')

class comment(models.Model):
     author = models.ForeignKey(User,on_delete=models.CASCADE)
     comment = models.TextField ()
     post = models.ForeignKey(Post,on_delete=models.CASCADE)
     created = models.DateField(default=timezone.now)
   
