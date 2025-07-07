"""
URL configuration for projet_python project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.shortcuts import render
from django.urls import path, include
from accounts import views
from accounts.views import custom_admin_logout as custom




urlpatterns = [
    path('admin/logout/', custom, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login'),
    path('accounts/', include('accounts.urls')),
    path('rh/', views.rh_page, name='rh_page'),
    path('employe/', views.employe_page, name='employe_page'),
    path('manager/', views.manager_page, name='manager_page'),
    
]
