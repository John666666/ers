#!/usr/bin/python
# -*-coding:utf8-*-
__author__ = 'John'

import time
import math
import hashlib

import requests
from requests import HTTPError

import sys_constant

'''
 网易云信操作类
'''
class NimUtils:

    def __init__(self):
        pass

    '''
        创建网易账号
        返回： 成功，返回网易生成的token；失败，返回None
    '''
    @classmethod
    def create_nim_user(cls, accid):
        url = "https://api.netease.im/nimserver/user/create.action"
        params = {"accid": accid}
        req = cls.request_nim(url, params)
        if req.status_code != 200:
            raise HTTPError("请求失败")
        ret_json = req.json()
        # {u'info': {u'accid': u'test_1', u'token': u'7d3b2c015e1377657c4ce4f71eb582d7', u'name': u''}, u'code': 200}
        # {u'code': 414, u'desc': u'already register'}
        try:
            return ret_json['info']['token']
        except:
            if ret_json["desc"].find("already") > -1:
                token = cls.refresh_nim_token(accid)
                cls.active_nim_user(accid)
                return token
            return None


    '''
        激活用户账号
        成功: 返回True, 失败：返回False
    '''
    @classmethod
    def active_nim_user(cls, accid):
        url = "https://api.netease.im/nimserver/user/unblock.action"
        params = {"accid": accid}
        req = cls.request_nim(url, params)
        if req.status_code != 200:
            raise HTTPError("请求失败")
        try:
            ret_json = req.json()
            return ret_json['code'] == 200
        except:
            return False

    '''
        禁用用户账号
        needkick: 是否立即踢掉用户
        成功： 返回True， 失败：返回False
    '''
    @classmethod
    def disable_nim_user(cls, accid, needkick=False):
        url = "https://api.netease.im/nimserver/user/block.action"
        params = {"accid": accid, "needkick": ("true" if needkick else "false")}
        req = cls.request_nim(url, params)
        if req.status_code != 200:
            raise HTTPError("请求失败")
        try:
            ret_json = req.json()
            return ret_json['code'] == 200
        except:
            return False

    '''
        刷新token
        成功： 返回刷新后的token； 失败： 返回None
    '''
    @classmethod
    def refresh_nim_token(cls, accid):
        url = "https://api.netease.im/nimserver/user/refreshToken.action"
        params = {"accid": accid}
        req = cls.request_nim(url, params)
        if req.status_code != 200:
            raise HTTPError("请求失败")
        try:
            ret_json = req.json()
            # {u'info': {u'accid': u'test_1', u'token': u'7d3b2c015e1377657c4ce4f71eb582d7', u'name': u''}, u'code': 200}
            return ret_json['info']['token']
        except:
            return None

    '''
        网易接口通用请求方法
    '''
    @classmethod
    def request_nim(cls, url, params):
        header = cls.getNimHeaderSign()
        return requests.post(url, data=params, headers=header)

    '''
        生成网易要求的签名
    '''
    @classmethod
    def getNimHeaderSign(cls):
        header = {}
        header["AppKey"] = sys_constant.nim_appKey
        header["CurTime"] = str(int(math.floor(time.time())))
        header["Nonce"] = str(int(time.time() * 1000))
        sha1 = hashlib.sha1("%s%s%s" % (sys_constant.nim_appSecret, header.get("Nonce"), header.get("CurTime")))
        header["CheckSum"] = sha1.hexdigest()
        return header

if __name__ == "__main__":
    nim = NimUtils()
    #print nim.getNimHeaderSign()
    # print nim.create_nim_user('test_2')
    print nim.refresh_nim_token('234234lkjkjwerf')
    # print nim.disable_nim_user('test_1')
    # print nim.active_nim_user('test_1')

