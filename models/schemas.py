#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     schemas
   Description :
   Author :       wang6237
   date：          2020/4/28 09:44
-------------------------------------------------
   Change Activity:
                   2020/4/28 09:44
-------------------------------------------------
"""
__author__ = 'wang6237'

from typing import List
from pydantic import BaseModel


class EnvBase(BaseModel):
    name: str
    comment: str = None
    template_name: List
    path: str
    content: str


class EnvCreate(EnvBase):
    pass


# 用于为Pydantic提供配置
class Env(EnvBase):
    id: int
    # template_name: str


class TemplateBase(BaseModel):
    name: str
    comment: str = None
    path: str
    content: str


class TemplateCreate(TemplateBase):
    pass


# 用于为Pydantic提供配置
class Template(TemplateBase):
    id: int


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password: str
    role: str


class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class Login(UserBase):
    password: str
