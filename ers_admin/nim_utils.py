#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

import time
import math
import hashlib

import requests
from requests import HTTPError
from .models import Client

import sys_constant
from requests import adapters


session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('http://', adapter)
session.mount('https://', adapter)


class NimUtils:
    u"""
        网易云信操作类
    """
    def __init__(self):
        pass

    @classmethod
    def create_nim_user(cls, accid):
        u"""
            创建网易账号
            返回： 成功，返回网易生成的token；失败，返回None
        """
        url = "https://api.netease.im/nimserver/user/create.action"
        params = {"accid": accid}
        req = cls.__request_nim(url, params)
        # {u'info': {u'accid': u'test_1', u'token': u'7d3b2c015e1377657c4ce4f71eb582d7', u'name': u''}, u'code': 200}
        # {u'code': 414, u'desc': u'already register'}
        try:
            if req.status_code != 200:
                raise HTTPError("请求失败")
            ret_json = req.json()
            return ret_json['info']['token']
        except:
            if ret_json["desc"].find("already") > -1:
                token = cls.refresh_nim_token(accid)
                cls.active_nim_user(accid)
                return token
            return None


    @classmethod
    def active_nim_user(cls, accid):
        u"""
            激活用户账号
            成功: 返回True, 失败：返回False
        """
        url = "https://api.netease.im/nimserver/user/unblock.action"
        params = {"accid": accid}
        req = cls.__request_nim(url, params)
        try:
            if req.status_code != 200:
                raise HTTPError("请求失败")
            ret_json = req.json()
            return ret_json['code'] == 200
        except:
            return False

    @classmethod
    def disable_nim_user(cls, accid, needkick=False):
        u"""
            禁用用户账号
            needkick: 是否立即踢掉用户
            成功： 返回True， 失败：返回False
        """
        url = "https://api.netease.im/nimserver/user/block.action"
        params = {"accid": accid, "needkick": ("true" if needkick else "false")}
        req = cls.__request_nim(url, params)
        try:
            if req.status_code != 200:
                raise HTTPError("请求失败")
            ret_json = req.json()
            return ret_json['code'] == 200
        except:
            return False

    @classmethod
    def refresh_nim_token(cls, accid):
        u"""
            刷新token
            成功： 返回刷新后的token； 失败： 返回None
        """
        url = "https://api.netease.im/nimserver/user/refreshToken.action"
        params = {"accid": accid}
        req = cls.__request_nim(url, params)
        try:
            if req.status_code != 200:
                raise HTTPError("请求失败")
            ret_json = req.json()
            # {u'info': {u'accid': u'test_1', u'token': u'7d3b2c015e1377657c4ce4f71eb582d7', u'name': u''}, u'code': 200}
            return ret_json['info']['token']
        except:
            return None

    @classmethod
    def force_add_nim_friends(cls, accid, faccid):
        u"""
            直接添加好友
            成功： 返回True； 失败： 返回False
        """
        url = "https://api.netease.im/nimserver/friend/add.action"
        params = {"accid": accid, "faccid": faccid, "type": 1}
        req = cls.__request_nim(url, params)
        if req.status_code != 200:
            raise HTTPError("请求失败")
        try:
            ret_json = req.json()
            return ret_json['info']['code'] == 200
        except:
            return False

    @classmethod
    def get_nim_friends(cls, accid):
        u"""
            获取好友列表
        """
        url = "https://api.netease.im/nimserver/friend/get.action"
        # createtime相当于好友关系的查询条件的创建时间，大于此时间的记录才会返回
        params = {"accid": accid, "createtime": 1504851372}
        req = cls.__request_nim(url, params)
        try:
            if req.status_code != 200:
                raise HTTPError("请求失败")
            ret_json = req.json()
            if ret_json['info']['code'] != 200:
                return False
            # 从网易获取所有好友账号， 然后从关联其它资料
            client_list = []
            for friend in ret_json["friends"]:
                faccid = friend.faccid
                if not faccid:
                    continue
                client = Client.getone(client_id=faccid)
                if client is not None:
                    client_list.append(client)

            # 按名称排序
            client_list.sort(key=lambda item:item.client_name)
            return client_list
        except:
            return False

    @classmethod
    def __request_nim(cls, url, params):
        u"""
            网易接口通用请求方法
        """
        header = cls.__get_nim_header_sign()
        return session.post(url, data=params, headers=header, timeout=5)


    @classmethod
    def __get_nim_header_sign(cls):
        u"""
            生成网易要求的签名
        """
        header = {}
        header["AppKey"] = sys_constant.nim_appKey
        header["CurTime"] = str(int(math.floor(time.time())))
        header["Nonce"] = str(int(time.time() * 1000))
        sha1 = hashlib.sha1("%s%s%s" % (sys_constant.nim_appSecret, header.get("Nonce"), header.get("CurTime")))
        header["CheckSum"] = sha1.hexdigest()
        return header

if __name__ == "__main__":
    nim = NimUtils()
    #print nim.__get_nim_header_sign()
    # print nim.create_nim_user('test_2')
    print nim.refresh_nim_token('234234lkjkjwerf')
    # print nim.disable_nim_user('test_1')
    # print nim.active_nim_user('test_1')

