#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

from django.test import TestCase
from .models import Client
from unittest import skip

# Create your tests here.
class ClientTest(TestCase):

    @skip("skip it")
    def test_client_getall(self):
        client_list = Client.getall()
        self.assertIsNotNone(client_list, "must not be None!")
        self.assertGreater(len(client_list), 1, "at least has one record")
        self.assertQuerysetEqual()

    def test_client_save(self):
        Client.save_client("离开教室夺开朗大方", "test_3")