#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.shortcuts import render
from django.http import HttpResponse
from ers_admin.models import Client
from ers_admin.nim_utils import NimUtils
import json
from .models import Locus
# Create your views here.

'''
    获取token， 给终端调用
'''
def get_nim_token(request):
    client_id = request.POST["client_id"]
    ret = None
    if client_id is not None:
        client = Client.getone(client_id=client_id)
        if client is not None:
            ret = {"result": {"token": client.token}, "code": 200}
    if not ret:
        ret = {"code": 300, "message": "获取token失败"}
    return HttpResponse(json.dumps(ret))

'''
    刷新token， 给终端调用
'''
def refresh_nim_token(request):
    client_id = request.POST["client_id"]
    ret = None
    if client_id is not None:
        client = Client.getone(client_id=client_id)
        if client is not None:
            token = NimUtils.refresh_nim_token(client_id)
            if token is not None:
                client.token = token
                client.save()
                ret = {"result": {"token": client.token}, "code": 200}
    if not ret:
        ret = {"code": 300, "message": "刷新token失败"}
    return HttpResponse(json.dumps(ret))

'''
    保存定位信息
'''
def save_locus(request):
    client_id = request.POST["client_id"]
    longitude = request.POST["longitude"]
    latitude = request.POST["latitude"]
    try:
        Locus.save_locus(client_id, longitude, latitude)
        return HttpResponse(json.dumps({"message": "保存成功", "code": 200}, ensure_ascii=False))
    except Exception, e:
        return HttpResponse(json.dumps({"message": "%s" % e, "code": 300}, ensure_ascii=False))

def get_nim_friends(request):
    client_id = request.POST["client_id"]
    ret = None
    try:
        client_list = NimUtils.get_nim_friends(client_id)
        if not client_list:
            ret = {"message": "获取好友失败", "code": 300}
        else:
            ret = {"result": client_list, "code": 200}
    except Exception, e:
        ret = {"message": "%s" % e, "code": 300}
    if not ret:
        ret = {"message": "获取好友失败", "code": 300}
    from ers_admin.models import ClientJSONEncoder
    return HttpResponse(json.dumps(ret, ensure_ascii=False, cls=ClientJSONEncoder))

service_handler_dic = {
    "get_nim_token": get_nim_token,
    "refresh_nim_token": refresh_nim_token,
    "save_locus": save_locus,
    "get_friends": get_nim_friends,
}

def dispatch(request):
    service = request.POST["service"]
    if service is None:
        return HttpResponse({"code": 300, "message": "service参数不能为空"})
    handler = service_handler_dic.get(service)
    if handler is None:
        return HttpResponse({"code": 300, "message": "不存在service: %s" % service})
    return handler(request)