#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     model
   Description :
   Author :       wang6237
   date：          2020/4/17 09:44
-------------------------------------------------
   Change Activity:
                   2020/4/17 09:44
-------------------------------------------------
"""
__author__ = 'wang6237'

from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapiConf.sqlite"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@172.16.2.44/config"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # sessionmaker 会话生成器
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()


# Dependency 依赖项
def get_db():
    try:
        db = db_session()  # 本地会话
        yield db
    finally:
        db.close()
        print('数据库已关闭')


class Environment(Base):
    __tablename__ = "environment"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, index=True)
    template_name = Column(String(180))
    path = Column(String(80))
    content = Column(String(4096))
    comment = Column(String(180))

    def __repr__(self):
        return '<Environment %r>' % self.name


class ServiceTemplate(Base):
    __tablename__ = "service-template"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, index=True)
    content = Column(String(2048))
    comment = Column(String(180))
    path = Column(String(80))

    def __repr__(self):
        return '<ServiceTemplate %r>' % self.name


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(80), unique=True, index=True)
    username = Column(String(80), index=True)
    password = Column(String)
    role = Column(String(80))

    def __repr__(self):
        return '<User %r>' % self.username
