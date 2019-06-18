"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url, include

from sign import views

urlpatterns = [
    path("api/", include("sign.urls", namespace="sign")),  # 接口地址
    path(r"", views.index),  # 127.0.0.1:8000
    path(r'admin/', admin.site.urls),
    # path(r'index/', views.index),  # 添加index/路径
    url(r"^index/$", views.index),  # 也可以的
    url(r"^logout/$", views.logout),  # 也可以的
    path("login_action/", views.login_action),  # 处理登录的路径
    path("event_manage/", views.event_manage),  # 登录成功，发布会页面
    path("guest_manage/", views.guest_manage),  # 登录成功，嘉宾页面
    path("accounts/login/", views.index),  # 登录页面都跳转到登录index界面
    path("search_name/", views.search_name),  # 跳转到发布会搜索结果列表
    path("search_guest_name/", views.search_guest_name),  # 跳转到嘉宾搜索结果列表
    re_path(r"sign_index/(?P<eid>[0-9]+)/", views.sign_index),  # 签到链接 re_path正则匹配
    re_path(r"sign_index_action/(?P<eid>[0-9]+)/", views.sign_index_action),  # 签到动作界面



]
