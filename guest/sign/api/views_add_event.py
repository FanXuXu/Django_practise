
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse
from sign.models import Event


# Create your views here.
# 新增发布会接口
def add_event(request):
    eid = request.POST.get("eid", "")
    name = request.POST.get("name", "")
    limit = request.POST.get("limit", "")
    status = request.POST.get("status", "")
    address = request.POST.get("address", "")
    start_time = request.POST.get("start_time", "")

    if eid == "" or name == "" or limit == "" or address == "" or start_time == "":
        data = {"status":10021, "message":"parameter error"}
        return JsonResponse(data=data)
    # 判断发布会是否存在，唯一的eid作为唯一标识
    result = Event.objects.filter(id=eid)
    if result:
        data = {"status":10022, "message":"发布会已存在，请检查项目编号"}
        return JsonResponse(data=data)
    # 判断发布会的名字是否重复
    result = Event.objects.filter(name=name)
    if result:
        data = {"status": 10023, "message": "发布会名称已经存在，请检查项目名称"}
        return JsonResponse(data=data)

    # 判断发布会名额限制是否设置
    # import unicodedata
    try:
        j_limit = int(limit)
    except ValueError as e:
        data = {"status": 10024, "message": "发布会人数限制异常"}
        return JsonResponse(data=data)
    else:
        if not isinstance(j_limit, int):
            data = {"status": 10024, "message": "发布会人数限制异常"}
            return JsonResponse(data=data)

    status = status if status else 1
    try:
        Event.objects.create(id=eid, name=name, limit=limit, status=int(status), address=address, start_time=start_time)
    except Exception as e:
        data = {"status": 10026, "message": e}
        return JsonResponse(data=data)
    return JsonResponse(data={"status": 200, "message": "发布会添加成功"})