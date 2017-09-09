# -*-coding:utf8-*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
from django.db.models.functions import Coalesce
import json

class Client(models.Model):
    u"""
        Client增删改查操作
    """
    client_id = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    token = models.CharField(max_length=200, null=True)
    status = models.IntegerField(default=0, help_text='终端接入状态: 0: 未激活 1: 正常')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

    @classmethod
    def getall(cls, **kwargs):
        return Client.objects.filter(**kwargs).order_by("id").reverse()

    @classmethod
    def getone(cls, **kwargs):
        try:
            return Client.objects.filter(**kwargs).get()
        except:
            return None

    @classmethod
    def save_client(cls, client_name, client_id, token=None, status=0):
        client = Client(client_name=client_name, token=token, status=status, client_id=client_id)
        try:
            client.save()
            return client
        except:
            return None

    @classmethod
    def update_token(cls, id, token, status=1):
        if not id:
            return False
        effect_rows = Client.objects.filter(id=id).update(token=token, status=status)
        return effect_rows > 0

    @classmethod
    def delete_client(cls, id):
        if not id:
            return False
        client = cls.getone(id=id)
        if client is not None:
            return client.delete() > 0
        return False

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_id', 'token', 'create_time', 'update_time',)
    search_fields = ('client_name',)

class ClientJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Client):
            return {"client_id": obj.client_id, "client_name": obj.client_name}
        return json.JSONEncoder.default(self, obj)
