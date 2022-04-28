from django.forms import ModelForm
from . models import Room,Post,User
from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host' , 'participants']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author' , 'likes' , 'dislikes' , 'title_tags']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']