#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Base
   Description :
   Author :       wang6237
   date：          2020/4/17 16:43
-------------------------------------------------
   Change Activity:
                   2020/4/17 16:43
-------------------------------------------------
"""
__author__ = 'wang6237'

# from werkzeug.security import generate_password_hash, check_password_hash
from jwt import PyJWTError
import requests
import json
import hashlib
import configparser
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, Request  # , status
from starlette import status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext  # passlib 处理哈希加密的包
from pydantic import BaseModel
from models import crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.model import get_db
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"# 密钥
ALGORITHM = "HS256"     # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 访问令牌过期分钟
LOGOUT_TOKEN_EXPIRE_SECONDS = 1     # 设置logout令牌过期时间
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")
# oauth2_scheme是令牌对象，token: str = Depends(oauth2_scheme)后就是之前加密的令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login")


config = configparser.ConfigParser()
try:
    config.read('./config/config.ini')
    # print(config.sections())
except Exception as e:
    print(e)


class Token(BaseModel):     # 令牌空壳
    token: str
    token_type: str


class TokenData(BaseModel):  # 令牌数据
    username: str = None


def hashTool(arg1, arg2):
    m1 = hashlib.md5()
    m2 = hashlib.md5()
    m1.update(arg1.encode('utf-8'))
    m2.update(arg2.encode('utf-8'))
    # print('Hash >>>>>>>>> ', m1.hexdigest(), m2.hexdigest())
    if m1.hexdigest() == m2.hexdigest():
        return True
    else:
        return False


# verify_password验证密码   plain_password普通密码      hashed_password哈希密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 获取密码哈希
def get_password_hash(password):
    return pwd_context.hash(password)


# 验证用户
def authenticate_user(fake_db, username: str, password: str):
    user = crud.get_user_by_name(fake_db, username)
    print(user)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user  # <class '__main__.UserInDB'>


# 创建访问令牌
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta # expire 令牌到期时间
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # print(encoded_jwt)
    return encoded_jwt


def revoking_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta # expire 令牌到期时间
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # print(encoded_jwt)
    return encoded_jwt


# 获取当前用户
def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
    except PyJWTError:
        print('ccccc')
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return payload


async def get_token_header(request: Request):
    # print(request.headers)
    try:
        token = request.headers['authorization'].split(' ')[1]
        r = get_current_user(token=token)
    except KeyError:
        raise HTTPException(status_code=403, detail="authorization header invalid, please do login")
    return r
    # if Authorization != "fake-super-secret-token":  # 假超密令牌
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")  # X令牌头无效
