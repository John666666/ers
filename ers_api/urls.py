#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_nim_token', views.get_nim_token, name='get_nim_token'),
    url(r'^refresh_nim_token', views.refresh_nim_token, name='refresh_nim_token'),
    url(r'^save_locus', views.save_locus, name='save_locus'),
]
