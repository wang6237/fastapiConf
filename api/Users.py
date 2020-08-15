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

from models import crud
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
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")  # 电子邮件已注册
    return crud.create_user(db=db, user=user)


# 编辑用户x
@router.put("/", response_model=schemas.User, dependencies=[Depends(get_token_header)])
async def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Username not found")  # 电子邮件已注册
    return crud.update_user(db=db, user=user)


# 删除用户
@router.delete("/")
async def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.del_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        pass


# 读取用户（用户ID范围）列表
@router.get("/", dependencies=[Depends(get_token_header)])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return {'total': len(users), 'items': users}


@router.get("/info", dependencies=[Depends(get_token_header)])
async def get_user_info():
    # print(11111)
    userinfo = {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin',
        'menu': [
        {
            'name': '名称',
            'path': '/test1',
            'component': '',
            'meta': {'title': 'Dashboard', 'icon': 'dashboard'}
        },
        {
            'name': '名称2',
            'path': '/test2',
            'component': '',
            'meta': {'title': 'Dashboard2', 'icon': 'dashboard2'}
        }
    ]
    }
    return userinfo


# 用ID的方式读取用户
@router.get("/{user_id}", response_model=schemas.User, dependencies=[Depends(get_token_header)])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 测试动态菜单，
@router.get("/menu/", dependencies=[Depends(get_token_header)])
async def get_menus(db: Session = Depends(get_db)):
    # print(user_id)
    # user_id = 1
    menuList = [{
        "children": [
          {
            "create_time": "2018-03-16 11:33:00",
            "menu_type": "C",
            "parent_id": 2,
            "menu_name": "数据监控",
            "icon": "#",
            "perms": "monitor:data:view",
            "order_num": 3,
            "menu_id": 15,
            "url": "/system/druid/monitor"
          }
        ],
        "parent_id": 0,
        "menu_name": "系统监控",
        "icon": "fa fa-video-camera",
        "perms": 'null',
        "order_num": 5,
        "menu_id": 2,
        "layout": True,
        "url": "/test"
      }]
    # db_user = crud.get_user(db, user_id=user_id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {'state': 0, 'menuList': menuList}


@router.get("/{username}", response_model=schemas.User, dependencies=[Depends(get_token_header)])
async def read_user(username: str, db: Session = Depends(get_db)):
    print(username)
    db_user = crud.get_user_by_name(db, username=username)
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


@router.post("/logout")
def doLogOut(request: Request):
    global token
    try:
        token = request.headers['authorization'].split(' ')[1]

    except KeyError:
        raise HTTPException(status_code=403, detail="authorization header invalid, please do login")
    finally:
        r = get_current_user(token=token)
        logout_token_expires = timedelta(seconds=LOGOUT_TOKEN_EXPIRE_SECONDS)
        token = create_access_token(data={"sub": 'admin'}, expires_delta=logout_token_expires)
        return {'type': 'success', 'msg': '退出成功'}




# @router.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


