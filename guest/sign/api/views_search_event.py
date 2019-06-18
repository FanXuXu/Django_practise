from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.http import JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from sign.models import Event


# Create your views here.
# 查询发布会接口
def search_event(request):
    eid = request.GET.get("eid", "")
    name = request.GET.get("name", "")

    if eid == "" and name == "":
        data = {"status":10021, "message": "parameter error!"}
        return JsonResponse()

    if eid != "":
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({"status":10022, "message": "query result is empty"})
        else:
            event["name"] = result.name
            event["limit"] = result.limit
            event["address"] = result.address
            event["start_time"] = result.start_time
            event["status"] = result.status
            return JsonResponse(data={"status": 200, "message": "发布会添加成功","content":event})

    if name != "":
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = dict()
                event["name"] = r.name
                event["limit"] = r.limit
                event["address"] = r.address
                event["start_time"] = r.start_time
                event["status"] = r.status
                datas.append(event)
            return JsonResponse({"status":200, "message": "success", "data": datas})
        else:
            return JsonResponse({"status":10022, "message": "query result is empty"})