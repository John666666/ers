#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'\.html', views.redirect_html, name='redirect'),
    url(r'^client_list', views.list_client, name='list_client'),
    url(r'^active_client', views.active_client, name='active_client'),
    url(r'^disable_client_list', views.disable_client, name='disable_client'),
    url(r'^add_client', views.save_client, name='save_client'),
    url(r'^delete_client$', views.delete_client, name='delete_client'),
    url(r'^delete_clients', views.delete_clients, name='delete_clients'),
    url(r'^update_client', views.update_client, name='update_client'),
    url(r'^client_to_update', views.client_to_update, name='client_to_update'),
    url(r'^browse_client', views.browse_client, name='browse_client'),
    url(r'^client_locus', views.client_locus, name='client_locus'),
    url(r'^nim_call', views.nim_call, name='nim_call'),
    url(r'^login$', views.login, name='login'),
]
