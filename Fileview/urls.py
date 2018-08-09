"""Fileview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from file import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^loadview$',views.index),
    url(r'^fileload$',views.fileload),
    url(r'^fileview$',views.fileview),#页面展示
    url(r'^queryfile$',views.queryfile),
    url(r'^login/$',views.loginManager,),
    url(r'^loginVerify$',views.loginVerify),
    url(r'^filedown$',views.filedown),
    url(r'^keyQuery$',views.keyQuery),
]
