#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from . import sys_constant

try:

    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print request.path
        if request.path.find("login") == -1 and request.path.find("ers_api") == -1 and request.path != '/Web/CheckCode/':
            user = request.session.get("user", None)
            if user and user == sys_constant.admin_count:
                pass
            else:
                return redirect("login.html")
                # return HttpResponseRedirect('login.html')
