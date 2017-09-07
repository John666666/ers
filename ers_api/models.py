#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.db import models
from django.contrib.admin import ModelAdmin

'''
    位置轨迹记录表
'''
class Locus(models.Model):
    client_id = models.CharField(max_length=200)
    longitude = models.DecimalField(decimal_places=10, max_digits=15)
    latitude = models.DecimalField(decimal_places=10, max_digits=15)
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
