from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns  =[

    path('',views.Home,name = 'Home'),
    path('login/' , views.LoginPage, name = 'login_page'),
    path('register/' , views.RegisterPage, name = 'register_page'),
    path('success/' , views.SuccessPage, name = 'success'),
    path('token/' , views.TokenPage, name ='token'),
    path('verify/<auth_token>',views.verify,name= 'verify'),
    path('error',views.ErrorPage, name = "error"),
   

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='base/Forgetpassword.html'),
    name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='base/success.html') ,
     name = "password_reset_done"),
    path('reset/<uidb64>/<token>',
    auth_views.PasswordResetConfirmView.as_view(template_name='base/Reset_password.html'),
    name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_done.html')
    ,name="password_reset_complete"),

    path('CreateRoom',views.CreateRoom,name='Create_room'),
    path('room/<str:pk>',views.room,name='room'),
    path('UpdateRoom/<str:pk>',views.UpdateRoom,name='UpdateRoom'),
    path('DeleteRoom/<str:pk>',views.DeleteRoom,name ='DeleteRoom'),
    path('DeleteMessage/<str:pk>',views.DeleteMessage,name ='delete-message'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('logout/', views.logoutPAGE, name="logout"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),


    #path('like/<int:pk>',views.LikeView,name='like_post'),
    path('create_post/',views.Create_Post,name='create_post'),
    path('update_post/<str:pk>',views.Update_Post,name='update_post'),
    path('delete_post/<str:pk>',views.Delete_Post,name='delete_post'),

    path('update-user/',views.updateUser,name='update-user'),

]