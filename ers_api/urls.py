#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dispatch, name='dispatch'),
]
