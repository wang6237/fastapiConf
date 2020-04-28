#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     User
   Description :
   Author :       wang6237
   date：          2020/4/17 10:33
-------------------------------------------------
   Change Activity:
                   2020/4/17 10:33
-------------------------------------------------
"""
__author__ = 'wang6237'

from models import curd
from models import schemas
from models.model import get_db
from typing import List
from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException, Header, Request
from sqlalchemy.orm import Session
from core.Base import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    LOGOUT_TOKEN_EXPIRE_SECONDS, get_current_user, get_token_header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from core.Base import oauth2_scheme
# from core.Base import LoginData
from time import sleep
router = APIRouter()


# 新建用户x
@router.post("/", response_model=schemas.User, dependencies=[Depends(get_token_header)])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = curd.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")  # 电子邮件已注册
    return curd.create_user(db=db, user=user)


# 读取用户（用户ID范围）
@router.get("/", dependencies=[Depends(get_token_header)])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = curd.get_users(db, skip=skip, limit=limit)
    return {'total': len(users), 'items': users}


@router.get("/info", dependencies=[Depends(get_token_header)])
async def get_user_info():
    # print(11111)
    userinfo = {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    }
    return userinfo


# 用ID的方式读取用户
@router.get("/{user_id}", response_model=schemas.User, dependencies=[Depends(get_token_header)])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = curd.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/{username}")
async def read_user(username: str, db: Session = Depends(get_db)):
    print(username)
    db_user = curd.get_user_by_name(db, username=username)
    print(db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/login", response_model=Token)
async def login_for_access_token(login_data: schemas.Login, db: Session = Depends(get_db)):
    # print(login_data)
    # 1、验证用户
    user = authenticate_user(db, login_data.username, login_data.password)  # 验证用户
    # 2、access_token_expires访问令牌过期
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # timedelta表示两个datetime对象之间的差异。（来自datetime包）
    # 3、create_access_token创建访问令牌
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # 返回
    return {"token": access_token, "token_type": "bearer"}


@router.post("/logout", dependencies=[Depends(get_token_header)])
def doLogOut(request: Request):
    token = request.headers['authorization'].split(' ')[1]
    # print(request.headers)
    r = get_current_user(token=token)
    # print(r, '>>>>>>>>>>>>>>>')
    logout_token_expires = timedelta(seconds=LOGOUT_TOKEN_EXPIRE_SECONDS)
    token = create_access_token(data={"sub": 'admin'}, expires_delta=logout_token_expires)
    # sleep(10)
    # print(get_current_user(token=token))
    return {'type': 'success', 'msg': '退出成功'}

# @router.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


