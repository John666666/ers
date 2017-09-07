#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.core import paginator

from .nim_utils import NimUtils
from . import sys_constant
from .models import Client

# Create your views here.

def index(request):
    return HttpResponse(render(request, "index.html"))

def list_client(request):
    client_id = request.POST.get("client_id")
    client_name = request.POST.get("client_name")
    status = request.POST.get("status")

    ## 查询条件
    kwargs = {}
    if client_id:
        kwargs["client_id"] = client_id
    if client_name:
        kwargs["client_name__contains"] = client_name
    if status is not None and status != "":
        kwargs["status"] = status

    currentPage = request.POST.get("pageNum", 1)
    client_list = Client.getall(**kwargs)
    pageObj = paginator.Paginator(client_list, sys_constant.pageSize)
    context = {"client_list": pageObj.page(currentPage), "currentPage": currentPage, "totalSize": pageObj.count,
               "client_id": client_id, "client_name": client_name, "status": status}
    return HttpResponse(render(request, "client_list.html", context))

def browse_client(request):
    client_list = Client.getall()
    context = {"client_list": client_list}
    return HttpResponse(render(request, "client_interaction.html", context))

def client_locus(request):
    return HttpResponse(render(request, "client_locus.html", context={}))

def nim_call(request):
    client_id = request.GET["client_id"]
    if client_id is None:
        return HttpResponse(json.dumps({"statusCode": "300", "message": "缺少终端号参数"}))

    client = Client.getone(client_id=client_id)
    if client is None:
        return HttpResponse(json.dumps({"statusCode": "300", "message": "终端%s不存在" % client_id}))
    token = client.token
    context = {"client_id": client_id, "token": token}
    return HttpResponse(render(request, "nim_call.html", context))


def save_client(request):
    client_id = request.POST['client_id']
    client_name = request.POST['client_name']
    ret = None
    try:
        if client_id:
            token = NimUtils.create_nim_user(client_id)
            if token:
                client = Client.save_client(client_name, client_id, token, status=1)
                if client:
                    ret = {"statusCode": "200", "message": "添加终端成功", "callbackType":"closeCurrent"}
    except Exception, e:
        print e
    if not ret:
        ret = {"statusCode": "300", "message": "添加终端失败"}
    return HttpResponse(json.dumps(ret))

def delete_client(request):
    id = request.GET['id']
    ret = None
    try:
        if id:
            client = Client.getone(id=id)
            if Client.delete_client(id):
                ret = {"statusCode": "200", "message": "删除终端成功"}
                NimUtils.disable_nim_user(client.client_id, needkick=True)
    except Exception, e:
        print e
    if not ret:
        ret = {"statusCode": "300", "message": "添加终端失败"}
    return HttpResponse(json.dumps(ret))

def delete_clients(request):
    ids = request.POST["ids"].split(",")
    count = 0
    if ids and len(ids) > 0:
        for id in ids:
            client = Client.getone(id=id)
            if client is None:
                continue
            if Client.delete_client(id):
                NimUtils.disable_nim_user(client.client_id, needkick=True)
                count += 1
    ret = {"statusCode": "200", "message": "成功删除%s条记录" % (str(count))}
    return HttpResponse(json.dumps(ret))

def active_client(request):
    id = request.GET['id']
    try:
        client = Client.getone(id=id)
        token = NimUtils.active_nim_user(client.client_id)
        Client.update_token(id, token)
        ret = {"statusCode": "200", "message": "终端已成功激活"}
    except Exception, e:
        ret = {"statusCode": "300", "message": "激活失败"}
        print e
    return HttpResponse(json.dumps(ret))

def disable_client(request):
    client_id = request.GET['id']
    try:
        client = Client.getone(id=client_id)
        NimUtils.disable_nim_user(client.get("client_id"))
        ret = {"statusCode":"200", "message":"终端已成功注销"}
    except:
        ret = {"statusCode":"300", "message":"注销失败"}
    return HttpResponse(json.dumps(ret))

def update_client(request):
    id = request.POST['id']
    client_name = request.POST['client_name']
    try:
        client = Client.getone(id=id)
        client.client_name = client_name
        client.update_time = datetime.now()
        client.save()
        ret = {"statusCode":"200", "message":"更新成功", "callbackType":"closeCurrent"}
    except:
        ret = {"statusCode":"300", "message":"更新失败"}
    return HttpResponse(json.dumps(ret))

def client_to_update(request):
    id = request.GET['id']
    print id
    client = Client.getone(id=id)
    context = {"client": client}
    return HttpResponse(render(request, "client_update.html", context))

def redirect_html(request):
    template_name = request.path[request.path.rfind("/")+1:]
    return HttpResponse(render(request, template_name))
