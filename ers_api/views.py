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



def index(request):
    return HttpResponse("welcome to ers_api! %s")


'''
    获取token， 给终端调用
'''
def get_nim_token(request):
    client_id = request.POST["client_id"]
    ret = None
    if client_id is not None:
        client = Client.getone(client_id=client_id)
        if client is not None:
            ret = {"token": client.token, "code": 200}
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
                ret = {"token": token, "code": 200}
    if not ret:
        ret = {"code": 300, "message": "刷新token失败"}
    return HttpResponse(json.dumps(ret))

'''
    保存定位信息
'''
def save_locus(request):
    try:
        client_id = request.POST["client_id"]
        longitude = request.POST["longitude"]
        latitude = request.POST["latitude"]
        Locus.save_locus(client_id, longitude, latitude)
        return HttpResponse({"message": "保存成功", "code": 200})
    except Exception, e:
        return HttpResponse({"message": "%s" % e, "code": 300})