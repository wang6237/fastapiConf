#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     init_db
   Description :
   Author :       wang6237
   date：          2020/6/8 16:14
-------------------------------------------------
   Change Activity:
                   2020/6/8 16:14
-------------------------------------------------
"""
__author__ = 'wang6237'



from models.schemas import UserCreate
from models.model import SessionLocal, Base, engine, get_db, db_session
from models.crud import get_user_by_name, create_user

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
# from app.db import base

ADMIN_USER = UserCreate(
            username='admin',
            email='xxxx@vip.qq.com',
            password='111111',
            role='admin',
        )

# print(type(ADMIN_USER))


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    # db_session = Session

    user = get_user_by_name(db_session, username=ADMIN_USER.username)
    user = False
    if not user:
        user = create_user(db_session, user=ADMIN_USER)


# db = get_db()
init_db(db_session)
