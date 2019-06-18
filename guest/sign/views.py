
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    # return HttpResponse("Hello Django!")
    return render(request, "index.html")


# 退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect("/index/")
    return response


def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            # HttpResponseRedirect 对路径进行重定向
            response = HttpResponseRedirect("/event_manage/")
            # response.set_cookie("user", username, 3600)  # 添加到浏览器cookie
            request.session["user"] = username  # 添加到浏览器session
            return response
        else:
            return render(request, "index.html", {"error": "username or pasword error !"})


@login_required
def event_manage(request):
    # username = request.COOKIES.get("user", "")  # 读取浏览器的cookie
    event_list = Event.objects.all()
    username = request.session.get("user", "")  # 读取浏览器的session
    # 分页
    paginator = Paginator(event_list, 2)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围内， 取最后一页面数据
        contacts = paginator.page(paginator.num_pages)

    return render(request, "event_manage.html", {"user": username,
                                                 "events": contacts})


@login_required
def guest_manage(request):
    # username = request.COOKIES.get("user", "")  # 读取浏览器的cookie
    guest_list = Guest.objects.all()
    username = request.session.get("user", "")  # 读取浏览器的session
    # 分页
    paginator = Paginator(guest_list, 2)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围内， 取最后一页面数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})


# 搜索发布会名称
@login_required
def search_name(request):
    username = request.session.get("user", "")
    search_name = request.GET.get("search_name", "")
    # search_id = request.GET.get("search_id", "")
    # search_dict = {"search_name": search_name, "search_id":search_id}
    event_list = Event.objects.filter(name__contains=search_name)
    # 分页
    paginator = Paginator(event_list, 2)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围内， 取最后一页面数据
        contacts = paginator.page(paginator.num_pages)
    # event_list = Event.objects.filter(**search_dict)
    print("发生大幅度{}".format(event_list))
    return render(request, "event_manage.html", {"user": username,
                                                 "events": contacts})

# 搜索嘉宾信息
@login_required
def search_guest_name(request):
    username = request.session.get("user", "")
    search_guest_name = request.GET.get("search_guest_name", "")
    # search_id = request.GET.get("search_id", "")
    # search_dict = {"search_name": search_name, "search_id":search_id}
    guest_list = Guest.objects.filter(realname__contains=search_guest_name)
    # event_list = Event.objects.filter(**search_dict)
    # print("发生大幅度{}".format(guest_list))
    # 分页
    paginator = Paginator(guest_list, 2)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围内， 取最后一页面数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})

# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, "sign_index.html", {"event": event})


# 签到页面
@login_required
@csrf_protect
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get("phone", "")
    sign_num = len(Guest.objects.filter(sign=1))
    guest_all = len(Guest.objects.filter(event_id=eid))
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, "sign_index.html", {"event": event,
                                                   "hint": "phone error.",
                                                   "sign_num": sign_num,
                                                   "guest_all": guest_all})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, "sign_index.html", {"event": event,
                                                   "hint": "phone or event id error.",
                                                   "sign_num": sign_num,
                                                   "guest_all": guest_all})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, "sign_index.html", {"event": event,
                                                   "hint": "user has sign in.",
                                                   "sign_num": sign_num,
                                                   "guest_all": guest_all})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign=1)
        return render(request, "sign_index.html", {"event": event,
                                                   "hint": "sign in success!",
                                                   "guest": result,
                                                   "sign_num": sign_num,
                                                   "guest_all": guest_all})
