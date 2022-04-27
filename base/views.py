import profile
from tkinter import EXCEPTION
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from rx import create
from tables import Description
from . models import Room,Topic,Profile,Message
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from . forms import RoomForm

# Create your views here.

def Home(request):
    rooms = Room.objects.all()[0:5]

    context = {'rooms' : rooms}
    return render(request,'base/Home.html',context)
    
def LoginPage(request):
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
            
            if authenticate(username=username,pasword1=password1) is None:
                messages.error(request,'check your password and email')
                return redirect('login_page')
            else:
                login(request,user)
                return redirect('home')
        return render(request,'base/login.html' )

def RegisterPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if password1 != password2:
            messages.error(request,"Password1 and Password2 doesn't match")
            return redirect('register')
        try:
             if User.objects.filter(username=username).first():
                    messages.error(request,"Username is already taken")
                    return redirect('registerPage')
             if User.objects.filter(email=email).first():
                    messages.error(request,"Email has been already used")
                    return redirect('registerPage')
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
    return render(request,'base/register.html' )


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




    
def ResetPassword(request,auth_token):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('passsword2')
        if password1 == password2:
                profile_object = Profile.objects.filter(auth_token=auth_token)
                if profile_object is None:
                    return redirect('error')
                else:
                    profile_object.user.set_password(password1)
                    profile_object.user.save()
                    return redirect('login_page')
        else:
            messages.error(request,"Your password doesn't match")
            return redirect('ResetPassword')
        

    return render(request,'base/Reset_password.html')

def SendMailToResetPaasword(email,token):
    subject = 'Reset Your password.'
    message = f'Reset password  by clicking link  http://127.0.0.1:8000/ResetPassword/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)

def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user  = User.objects.filter(email=email)
        if user is  None:
            messages.error(request,'Email not found')
            return redirect('forgetpassword')
        else:
           auth_token = str(uuid.uuid4())
           SendEmailAfterRegistration(email,auth_token)
           profile_object = Profile.objects.filter(user__email=email)
           if profile_object is not None:
                profile_object.auth_token = auth_token
                
                return redirect('success')
           
    return render(request,'base/Forgetpassword.html')   
        
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


def userProfile(request,pk):
    user = user.objects.get(id=pk)
    room = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.object.all()

    context = {'room':room, 'room_messages' : room_messages , 'topics' : topics  , 'user' : user}

    return render(request,'base/profile.html' , context)

def add_profile(request):
     pass


