#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       wang6237
   date：          2020/4/17 10:02
-------------------------------------------------
   Change Activity:
                   2020/4/17 10:02
-------------------------------------------------
"""
__author__ = "wang6237"

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api import Users, Template, Env
from core.Base import *

app = FastAPI()
app.include_router(Users.router, prefix='/v1/user', tags=["user"])
app.include_router(Template.router, prefix="/v1/template", tags=["template"], dependencies=[Depends(get_token_header)])
app.include_router(Env.router, prefix="/v1/env", tags=["env"])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
