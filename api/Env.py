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
from typing import List
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


@router.delete("/{env_id}")
async def deleteEnv(env_id: int, db: Session = Depends(get_db)):
    env = crud.getEnvs_by_id(db, env_id=env_id)
    if env:
        crud.deleteEnv(db, env_id=env_id)
        return {'type': 'success', 'msg': '删除成功'}
    else:
        return {'type': 'error', 'msg': '删除失败，数据不存在'}


@router.get("/{env_id}")
async def getEnv(env_id: int, db: Session = Depends(get_db)):
    r = crud.getEnvs_by_id(db, env_id=env_id)
    if r:
        return {'type': 'success', 'msg': r}
    else:
        return {'type': 'error', 'msg': '数据不存在'}


@router.put("/")
async def editEnv(env: schemas.Env, db: Session = Depends(get_db)):
    e = crud.getEnvs_by_name(db, env_name=env.name)
    print("DB >>>>", e.template_name)
    # print("Request >>>>", env.content)
    print("Request >>>>", env.template_name)
    c = []
    path = env.path
    if path[:-1] == '/':
        pass
    else:
        path = path + '/'

    if e:
        new = json.loads(e.content)
        # raise HTTPException(status_code=400, detail="The template name already exists")
        # 循环db中template_name的数据，
        # if env.template_name
        for name in json.loads(e.template_name):
            # print(0, name, env.template_name)
            # db中存在，而新数据中不存在，这是减少了服务模板，这是要删除对应的数据，template_name和content中的数据
            if name not in env.template_name:
                # 删除template_name字段中对应的内容
                # print(json.loads(e.template_name), name)
                template_name_list = json.loads(e.template_name)
                template_name_list.remove(name)
                # 删除content字段中对应的内容
                for i, cc in enumerate(new):
                    # print(i, name, cc['name'])
                    print("Path >>>>> ", cc['path'])
                    etcdServer = GetEtcdApi(cc['path'])
                    if name == cc['name']:
                        new.pop(i)
                        r = etcdServer.DeleteKye()
        # print("已删掉>>>>>>>> ", e.content)
        # 循环新数据中的template_name字段，是否已存在在DB中
        for n in env.template_name:
            if n not in e.template_name:
                templ = crud.getTemplate_by_name(db, template_name=n)
                if templ.path[0] == '/':
                    templ.path = templ.path[1:]
                    t = {
                        'name': n,
                        'path': path + templ.path,
                        'content': templ.content
                    }
                    new.append(t)
                else:
                    t = {
                        'name': n,
                        'path': path + templ.path,
                        'content': templ.content
                    }
                    new.append(t)
                print('template>>>>>', new)
            # else:
            #     print(1, c, new)
            #     new = json.dumps(new)
            #     c.append(new)
        env.content = json.dumps(new)
        env.template_name = json.dumps(env.template_name)
        r = crud.editEnv(db, env=env)
        # return t
        print(r)
        if r:
            return {'type': 'success', 'msg': '编辑成功'}
        else:
            return {'type': 'error', 'msg': '更新失败'}
    else:
        return {'type': 'error', 'msg': '更新失败,数据不存在'}


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
        env.template_name = json.dumps(env.template_name)

        # env.template_name = json.dumps(env.template_name)
        print("HHHHH>>>>", env.template_name)
        crud.createEnv(db, env=env)
        # return t
        return {'type': 'success', 'msg': '增加成功'}
    # return {'type': 'success', 'msg': '增加成功'}


@router.post("/sync/")
async def syncEtcd(template: schemas.TemplateBase, db: Session = Depends(get_db)):
    etcdServer = GetEtcdApi(template.path)
    c = etcdServer.CreateKey(template.content, mkdir=False)
    return {'type': 'success', 'msg': '同步成功！'}


@router.delete("/sync/{env_id}")
async def syncEtcdDelete(env_id: int, template: schemas.TemplateBase, db: Session = Depends(get_db)):
    envInfo = crud.getEnvs_by_id(db, env_id=env_id)
    etcdServer = GetEtcdApi(template.path)
    if envInfo is None:
        return {'type': 'error', 'msg': '数据不存在，无法删除'}
    else:
        data = json.loads(envInfo.content)
        for index, i in enumerate(data):
            if i['path'] == template.path:
                data.pop(index)
                r = etcdServer.DeleteKye()
        envInfo.content = json.dumps(data)
        print("envInfo >>>> ", envInfo)
        e = crud.editEnv(db, env=envInfo)
        print(e)
        return {'type': 'success', 'msg': '删除成功'}


@router.put("/sync/state/{env_id}")
async def syncEtcdState(env_id: int, template: schemas.TemplateBase, db: Session = Depends(get_db)):
    # print(env_id)
    envInfo = crud.getEnvs_by_id(db, env_id=env_id)
    if envInfo is None:
        return {'type': 'error', 'msg': '数据不存在，无法同步'}
    # print(template.path)
    etcdServer = GetEtcdApi(template.path)
    c = etcdServer.GetKey()
    print(c)
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


@router.post("/get_etcd/")
async def getEtcdData(template: schemas.TemplateBase):
    print(template)
    etcdServer = GetEtcdApi(template.path)
    c = etcdServer.GetKey()
    if c['status_code'] == 200:
        if 'errorCode' in c['data'].keys():
            return {'state': 1, 'items': [c['data']['errorCode']]}
        else:
            return {'state': 0, 'items': c['data']['node']['value']}
    else:
        return {'state': 1, 'items': []}


@router.put("/update_etcd/{env_id}")
async def updateEtcdData(env_id: int, template: schemas.TemplateBase, db: Session = Depends(get_db)):
    """
    1、先更新etcd中的数据，在更新db中的数据
    2、如果出错，就回滚。
    :param db: 数据库
    :param env_id: 更新数据库时需要
    :param template: 更新数据
    :return: type [success/error; msg [成功/失败]
    """
    print(env_id)
    etcdServer = GetEtcdApi(template.path)
    c = etcdServer.UpdateKey(template.content)
    if c['status_code'] == 200:
        r = crud.getEnvs_by_id(db, env_id)
        print(r.template_name)
        if r:
            template_list = []
            if template.name in json.dumps(r.template_name):
                # print(template.name)
                for t in json.loads(r.content):
                    # print(t['name'])
                    if template.name == t['name']:
                        t['content'] = template.content
                    template_list.append(t)
                r.content = json.dumps(template_list)
                print(r)
                crud.editEnv(db, r)
        return {'type': 'success', 'msg': '更新成功'}
    else:
        return {'type': 'error', 'msg': '更新失败'}

