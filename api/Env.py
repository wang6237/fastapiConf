#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Item
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
import json
from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from core.etcd import GetEtcdApi
from core.Base import hashTool
from fastapi.encoders import jsonable_encoder
# from starlette.requests import Request


router = APIRouter()


@router.get("/")
async def getEnvList(page: int = 0, size: int = 100, db: Session = Depends(get_db)):
    env_lists = crud.getEnvs(db, size=size, page=page)
    env_list = []
    if len(env_lists) == 0:
        return {'total': 0, 'items': []}
    else:
        for e in env_lists:
            i = {'name': e.name, 'path': e.path, 'id': e.id,
                 'content': json.loads(e.content), 'comment': e.comment}
            env_list.append(i)
    # return jsonify({'total': len(env_list), 'items': env_list})
    return {'total': len(env_list), 'items': env_list}


@router.get("/{env_id}")
async def getEnv(env_id: int, db: Session = Depends(get_db)):
    r = crud.getEnvs_by_id(db, env_id=env_id)
    if r:
        return {'type': 'success', 'msg': r}
    else:
        return {'type': 'error', 'msg': '数据不存在'}


@router.put("/{env_id}")
async def editEnv(env_id: int, env: schemas.Env, db: Session = Depends(get_db)):
    temp = crud.getEnvs_by_id(db, env_id=env_id)
    # print(temp.name)
    if temp:
        r = crud.editEnv(db, env_id=env_id, env=env)
        if r:
            return {'type': 'success', 'msg': '编辑成功'}
        else:
            return {'type': 'error', 'msg': '编辑失败'}
    else:
        return {'type': 'error', 'msg': '模板不存在'}


@router.post("/")
async def createEnv(env: schemas.EnvCreate, db: Session = Depends(get_db)):
    print(env)
    # print(db)
    e = crud.getEnvs_by_name(db, env_name=env.name)
    # print(e)
    if e:
        # raise HTTPException(status_code=400, detail="The template name already exists")
        return {'type': 'error', 'msg': '增加失败,已存在'}
    else:
        c = []
        path = env.path
        if path[:-1] == '/':
            pass
        else:
            path = path + '/'
        # print(env)
        for name in env.template_name:
            templ = crud.getTemplate_by_name(db, template_name=name)
            if templ.path[0] == '/':
                templ.path = templ.path[1:]
                t = {
                    'name': name,
                    'path': path + templ.path,
                    'content': templ.content
                }
                c.append(t)
            else:
                t = {
                    'name': name,
                    'path': path + templ.path,
                    'content': templ.content
                }
                c.append(t)
            print('template>>>>>', c)
        env.content = json.dumps(c)
        crud.createEnv(db, env=env)
        # return t
        return {'type': 'success', 'msg': '增加成功'}
    # return {'type': 'success', 'msg': '增加成功'}


@router.delete("/{env_id}")
async def deleteEnv(env_id: int, db: Session = Depends(get_db)):
    env = crud.getEnvs_by_id(db, env_id=env_id)
    if env:
        crud.deleteEnv(db, env_id=env_id)
        return {'type': 'success', 'msg': '删除成功'}
    else:
        return {'type': 'error', 'msg': '删除失败，数据不存在'}


@router.post("/sync/")
async def syncEtcd(template: schemas.TemplateBase, db: Session = Depends(get_db)):
    # envInfo = crud.getEnvs_by_id(db, env_id=env_id)
    print(template.path)
    etcdServer = GetEtcdApi(template.path)
    c = etcdServer.CreateKey(template.content, mkdir=False)
    print(c)
    return {'type': 'success', 'msg': '同步成功！'}


@router.delete("/sync/")
async def syncEtcdDelete():
    pass


@router.put("/sync/state/{env_id}")
async def syncEtcdState(env_id: int, template: schemas.TemplateBase, db: Session = Depends(get_db)):
    envInfo = crud.getEnvs_by_id(db, env_id=env_id)
    print(template.path)
    etcdServer = GetEtcdApi(template.path)
    c = etcdServer.GetKey()
    if c['status_code'] == 200:
        if 'errorCode' in c['data'].keys():
            return {'state': 1, 'items': [c['data']['errorCode']]}
        r = hashTool(template.content, c['data']['node']['value'])
        if r:
            return {'state': 0, 'items': c['data']['node']['value']}
        else:
            return {'state': 1, 'items': c['data']['node']['value']}
    else:
        return {'state': 1, 'items': []}
