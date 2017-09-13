#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.db import models
from django.contrib.admin import ModelAdmin
import json

'''
    位置轨迹记录表
'''
class Locus(models.Model):
    client_id = models.CharField(max_length=200, db_index=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    create_time = models.DateTimeField(auto_now=True)

    @classmethod
    def save_locus(cls, client_id, longitude, latitude):
        locus = Locus(client_id=client_id, longitude=longitude, latitude=latitude)
        return locus.save()

    @classmethod
    def getall(cls, **kwargs):
        return Locus.objects.filter(**kwargs)

class LocusAdmin(ModelAdmin):
    list_display = ("client_id", "longitude", "latitude", "create_time")
    search_fields = ("client_id", )

class LocusJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Locus):
            return {"longitude": obj.longitude, "latitude": obj.latitude, "create_time": obj.create_time.strftime("%Y/%m/%d %H:%M:%S")}
        return json.JSONEncoder.default(self, obj)
