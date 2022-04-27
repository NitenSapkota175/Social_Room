from django.urls import path
from . import views
urlpatterns  =[

    path('',views.Home,name = 'Home'),
    path('login/' , views.LoginPage, name = 'login_page'),
    path('register/' , views.RegisterPage, name = 'register_page'),
    path('success/' , views.SuccessPage, name = 'success'),
    path('token/' , views.TokenPage, name ='token'),
    path('verify/<auth_token>',views.verify,name= 'verify'),
    path('error',views.ErrorPage, name = "error"),
    path('forgetpassword/',views.ForgetPassword,name='forgetpassword'),
    path('ResetPassword/<auth_token>',views.ResetPassword,name='ResetPassword'),


    path('CreateRoom',views.CreateRoom,name='Create_room'),
    path('room/<str:pk>',views.room,name='room'),
    path('UpdateRoom/<str:pk>',views.UpdateRoom,name='UpdateRoom'),
    path('DeleteRoom/<str:pk>',views.DeleteRoom,name ='DeleteRoom'),
    path('DeleteMessage/<str:pk>',views.DeleteMessage,name ='delete-message'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),


]