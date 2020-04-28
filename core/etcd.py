#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     etcd
   Description :
   Author :       wang6237
   date：          2020/4/17 16:41
-------------------------------------------------
   Change Activity:
                   2020/4/17 16:41
-------------------------------------------------
"""
__author__ = 'wang6237'
import requests
import json
import hashlib
import configparser

from  core.Base import config

class GetEtcdApi(object):
    """
    (host=(('127.0.0.1', 4001), ('127.0.0.1', 4002), ('127.0.0.1', 4003)))
    """

    def __init__(self, key):
        # config.get("etcd","etcdBaseUrl")
        self.url = config.get("etcd", "etcdBaseUrl") + key
        super(GetEtcdApi, self).__init__()

    def GetKey(self):
        try:
            r = requests.get(self.url)
            d = {'status_code': 200, 'data': r.json()}
            return d
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}

    def DeleteKye(self):
        try:
            r = requests.delete(self.url + '?dir=true&recursive=true')
            # print(r.status_code)
            return r.json()
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}

    def UpdateKey(self, value):
        data = {'value': value}
        try:
            r = requests.put(self.url, data=data)
            # print(r.status_code)
            return r.json()
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}

    def CreateKey(self, value, mkdir):
        if mkdir:
            data = {'dir': mkdir}
            try:
                r = requests.put(self.url, data=data)
                # print(r.status_code)
                return r.json()
            except requests.exceptions.ConnectionError:
                return {'status_code': -1, 'data': '无法连接到etcd....'}
        else:
            data = {'value': value}
            try:
                r = requests.put(self.url, data=data)
                print(r.status_code)
                return r.json()
            except requests.exceptions.ConnectionError:
                return {'status_code': -1, 'data': '无法连接到etcd....'}

    def GetAllKey(self):
        try:
            r = requests.get(self.url + '/')
            return r.json()
        except requests.exceptions.ConnectionError:
            return {'status_code': -1, 'data': '无法连接到etcd....'}
