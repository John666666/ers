#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

import json
from datetime import datetime

from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.core import paginator

from .nim_utils import NimUtils
from . import sys_constant
from .models import Client
from ers_api.models import Locus, LocusJSONEncoder
from django.shortcuts import HttpResponseRedirect



# Create your views here.

def index(request):
    context = {"user": request.session.get("user")}
    return HttpResponse(render(request, "index.html", context))


def login(request):
    client_id = request.POST["client_id"]
    pwd = request.POST["pwd"]
    ret = None
    if client_id is None or pwd is None:
        ret = {"code": 403, "message": "用户名或密码为空!"}
    else:
        if client_id != sys_constant.admin_count or pwd != sys_constant.admin_pwd:
            ret = {"code": 403, "message": "用户名或密码错误!"}
        else:
            client = Client.getone(client_id=client_id)
            if client is None:
                # 初始化admin账户
                token = NimUtils.create_nim_user(client_id)
                if token:
                    client_list = Client.getall()  # 获取所有已存在的用户
                    client = Client.save_client("管理员", client_id, token, status=1)
                    if client:
                        # 新用户保存成功后， 和之前的所有用户添加好友关系
                        if client_list:
                            for already_client in client_list:
                                NimUtils.force_add_nim_friends(client_id, already_client.client_id)
            request.session["user"] = client_id
            ret = {"code": 200, "message": "登录成功!"}
    if not ret:
        ret = {"code": 300, "message": "登录失败!"}
    return HttpResponse(json.dumps(ret))


def logout(request):
    request.session.clear()
    return redirect("login.html")
    # return HttpResponse(render(request, "logout.html"))


def list_client(request):
    u"""
        分布查询终端
    """
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
    client_list = Client.getall(**kwargs).exclude(client_id=sys_constant.admin_count)
    pageObj = paginator.Paginator(client_list, sys_constant.pageSize)
    context = {"client_list": pageObj.page(currentPage), "currentPage": currentPage, "totalSize": pageObj.count,
               "client_id": client_id, "client_name": client_name, "status": status}
    return HttpResponse(render(request, "client_list.html", context))


def browse_client(request):
    u"""
        不分布查询所有终端
    """
    client_list = Client.getall().exclude(client_id=sys_constant.admin_count).exclude(status=0)
    context = {"client_list": client_list}
    return HttpResponse(render(request, "client_interaction.html", context))


def client_locus(request):
    u"""
        查看指定终端轨迹
    """
    client_id = request.GET["client_id"]
    if client_id:
        #import time
        #create_time__gte=time.strftime("%Y-%m-%d", time.localtime())
        locus_list = list(Locus.getall(client_id=client_id, ))
        context = {"locus_list": json.dumps(locus_list, cls=LocusJSONEncoder, ensure_ascii=False)}
    return HttpResponse(render(request, "client_locus.html", context))

def nim_call(request):
    u"""
        呼叫终端
    """
    client_id = request.GET["client_id"]
    if client_id is None:
        return HttpResponse(json.dumps({"statusCode": "300", "message": "缺少终端号参数"}))
    # 获取本方账号信息
    client = Client.getone(client_id=sys_constant.admin_count)
    if client is None:
        return HttpResponse(json.dumps({"statusCode": "300", "message": "请登录后再进行此操作"}))
    accid = client.client_id
    token = client.token
    context = {"accid": accid, "token": token, "faccid": client_id}
    return HttpResponse(render(request, "nim_call.html", context))


def nim_call_inner(request):
    client_id = request.GET["client_id"]
    if client_id is None:
        return HttpResponse(json.dumps({"statusCode": "300", "message": "缺少终端号参数"}))
    # 获取本方账号信息
    client = Client.getone(client_id=sys_constant.admin_count)
    if client is None:
        return HttpResponse(json.dumps({"statusCode": "300", "message": "请登录后再进行此操作"}))
    accid = client.client_id
    token = client.token
    context = {"accid": accid, "token": token, "faccid": client_id}
    return HttpResponse(render(request, "nim_call_inner.html", context))


def save_client(request):
    u"""
        添加终端
    """
    client_id = request.POST['client_id']
    client_name = request.POST['client_name']
    ret = None
    try:
        if client_id:
            token = NimUtils.create_nim_user(client_id)
            if token:
                client_list = Client.getall()  # 获取所有已存在的用户
                client = Client.save_client(client_name, client_id, token, status=1)
                if client:
                    # 新用户保存成功后， 和之前的所有用户添加好友关系
                    if client_list:
                        for already_client in client_list:
                            NimUtils.force_add_nim_friends(client_id, already_client.client_id)

                    ret = {"statusCode": "200", "message": "添加终端成功", "callbackType": "closeCurrent"}
    except Exception, e:
        print e
    if not ret:
        ret = {"statusCode": "300", "message": "添加终端失败"}
    return HttpResponse(json.dumps(ret))


def delete_client(request):
    u"""
        删除终端
    """
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
    u"""
        批量删除终端
    """
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
    u"""
        激活终端
    """
    id = request.GET['id']
    ret = None
    try:
        client = Client.getone(id=id)
        if NimUtils.active_nim_user(client.client_id):
            client.status = 1
            client.save()
            ret = {"statusCode": "200", "message": "终端已成功激活"}
    except Exception, e:
        ret = {"statusCode": "300", "message": "激活失败"}
        print e
    if not ret:
        ret = {"statusCode": "300", "message": "激活失败"}
    return HttpResponse(json.dumps(ret))


def disable_client(request):
    u"""
        锁定终端
    """
    client_id = request.GET['id']
    try:
        client = Client.getone(id=client_id)
        if NimUtils.disable_nim_user(client.client_id):
            client.status = 0
            client.save()
            ret = {"statusCode": "200", "message": "终端已成功注销"}
    except Exception, e:
        print e
        ret = {"statusCode": "300", "message": "注销失败"}
    if not ret:
        ret = {"statusCode": "300", "message": "注销失败"}
    return HttpResponse(json.dumps(ret))


def update_client(request):
    u"""
        更新终端
    """
    id = request.POST['id']
    client_name = request.POST['client_name']
    try:
        client = Client.getone(id=id)
        client.client_name = client_name
        client.update_time = datetime.now()
        client.save()
        ret = {"statusCode": "200", "message": "更新成功", "callbackType": "closeCurrent"}
    except:
        ret = {"statusCode": "300", "message": "更新失败"}
    return HttpResponse(json.dumps(ret))


def client_to_update(request):
    u"""
        跳转到更新页面
    """
    id = request.GET['id']
    print id
    client = Client.getone(id=id)
    context = {"client": client}
    return HttpResponse(render(request, "client_update.html", context))


def redirect_html(request):
    template_name = request.path[request.path.rfind("/") + 1:]
    return HttpResponse(render(request, template_name))
