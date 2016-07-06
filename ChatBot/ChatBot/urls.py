#coding: utf-8


"""ChatBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from views import *
from stranger import views as strangerViews
from robot import views as robotViews
import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^index/$',index),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^index/stranger/$', strangerViews.stranger),
    url(r'^index/robot/$', robotViews.robot),
    url(r'^index/robot/chatting/$', robotViews.answerFromCh2r),
    url(r'^index/$', index),
    url(r'^index/stranger/history/$', strangerViews.stranger_history),
    url(r'^index/stranger/filedownload/$', strangerViews.big_file_download),	#跳转到download页面之后由get处理
    url(r'^index/stranger/filerecive/$', strangerViews.file_receive),

    ]