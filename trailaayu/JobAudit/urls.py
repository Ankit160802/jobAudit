

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index1'),
    path('login_user',views.login_user,name='login'),
    path('resumechecker',views.resumechecker,name='resume'),
    path('logout_user',views.logout_user,name='logout'),
    path('register_user',views.register_user,name='register'),
    path('activate/<uidb64>/<token>',views.activate,name="activate")
]