import profile
from tkinter import EXCEPTION
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse

from django.contrib import messages
from rx import create
from django.urls import reverse,reverse_lazy
from tables import Description
from . models import Room,Topic,Profile,Message,Post,User
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from . forms import PostForm, RoomForm,UserForm
from django.db.models import Q

# Create your views here.

###HOme####



def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/Home.html', context)
 
    return render(request, 'base/Home.html')

######   Authentication #######



def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password')
            
            user = User.objects.filter(username=username).first()
            if user is None:
                messages.error(request,'User not found')
                return redirect('login_page')
            
            
            profile_object = Profile.objects.filter(user = user).first()
            if not profile_object.is_verified:
                messages.error(request,'Your account  is not verified')
                return redirect('login_page')
            
            if authenticate(username=username,password=password1) is None:
                messages.error(request,'check your password and email')
                return redirect('login_page')
            else:
                login(request,user)
                return redirect('Home')
    return render(request,'base/login.html' )

def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if password1 != password2:
            messages.error(request,"Password1 and Password2 doesn't match")
            return redirect('register_page')
        try:
             if User.objects.filter(username=username).first():
                    messages.error(request,"Username is already taken")
                    return redirect('register_page')
             if User.objects.filter(email=email).first():
                    messages.error(request,"Email has been already used")
                    return redirect('register_page')
             user_obj = User.objects.create(username=username,email=email)
             user_obj.set_password(password1)
             user_obj.save()
             auth_token = str(uuid.uuid4())
             profile_object = Profile.objects.create(user = user_obj,auth_token = auth_token)
             profile_object.save()

             SendEmailAfterRegistration(email,auth_token)
             
             return redirect('token')
        except Exception as E:
            print(E)
    return render(request,'base/register.html')


def logoutPAGE(request):
    
        logout(request)
        return redirect('Home')

def SuccessPage(request):
    return render(request,'base/success.html')

def TokenPage(request):
    return render(request,'base/token.html')


def SendEmailAfterRegistration(email,token):
    subject = 'Thankyou for creating an account.'
    message = f'verify your account by clicking link  http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)

def verify(request,auth_token):

 try:
        profile_object = Profile.objects.filter(auth_token=auth_token).first()
        if profile_object:
            if profile_object.is_verified:
                messages.success(request,'Your account is already verified')
                return redirect('login_page')
            profile_object.is_verified = True
            profile_object.save()
            messages.success(request, 'Your email had been register.')
            return redirect('login_page')
        else:
            return redirect('error')
 except Exception as p:
     print(p)

def ErrorPage(request):
    return render(request,'base/error.html')



 
   
###################### End of email login and register ######################################


# CRUD ROOM OPERATIONS ################################

def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name  = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('Home')

    context = {'form' : form ,'topics' : topics}
    return render(request,'base/room_form.html' , context)


def room(request,pk):
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all()
        participants = room.participants.all()
        
        if request.method == 'POST':
            Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST.get('body')

            )
            room.participants.add(request.user)
            return redirect('room',room.id)
        context = {'room' : room,'room_messages' : room_messages ,'participants': participants }
        return  render(request,'base/room.html',context)


def UpdateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        messages.error(request,"You're not allowed")
        return redirect('error')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description') 
        room.save()
        return redirect('Home')
    
    context = {'form' : form , 'room' : room,'topics' : topics}
    return render(request,'base/room_form.html',context)

def DeleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request,"You're not allowed to delete this room")
    
    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    
    
    return render(request,'base/delete.html',{'obj' : room})

def DeleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')

    if request.method == 'POST':
        message.delete()
        return redirect('Home',)
    return render(request,'base/delete.html' , {'obj' : message})

def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

def add_profile(request):
     pass

'''def LikeView(request,pk):
    post = get_object_or_404(Post,id=request.post.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('Home',args=[str(pk)]))  
'''
def Create_Post(request):
    form = PostForm()
    if request.method == 'POST':
        body = request.POST.get('body')
        author = request.user
        post = Post.objects.create(body=body,author=author)
        
        redirect('Home')
    return render(request,'base/create_post.html',{'form' : form })

def Update_Post(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.user !=  post.author:
        messages.error(request,"You're not allowed")
        return redirect('error')
    if request.method == 'POST':
        post.body = request.POST.get('body') 
        post.save()
        return redirect('Home')

    return render(request,'base/update_post.html' , {'form' : form})

def Delete_Post(request,pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        messages.error(request,"You're not allowed to delete this room")
        return redirect('error')
    
    if request.method == 'POST':
        post.delete()
        return redirect('Home')
    return render(request,'base/delete.html',{'obj' : room})
###post ######



### user profile###########

def UpdateProfile(request):
    pass

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
