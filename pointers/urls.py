from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static #this helps you set the url for static files 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),

]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)