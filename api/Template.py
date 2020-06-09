#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Template
   Description :
   Author :       wang6237
   date：          2020/4/17 16:05
-------------------------------------------------
   Change Activity:
                   2020/4/17 16:05
-------------------------------------------------
"""
__author__ = 'wang6237'

from models import crud
from models import schemas
from models.model import get_db

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/")
async def getTemplateList(page: int = 0, size: int = 100, db: Session = Depends(get_db)):
    r = crud.getTemplates(db, size=size, page=page)
    return {'total': len(r), 'items': r}


@router.get("/{template_id}")
async def getTemplate(template_id: int, db: Session = Depends(get_db)):
    r = crud.getTemplate_by_id(db, template_id=template_id)
    if r:
        return {'type': 'success', 'msg': r}
    else:
        return {'type': 'error', 'msg': '数据不存在'}


@router.put("/{template_id}")
async def editTemplate(template_id: int, template: schemas.Template, db: Session = Depends(get_db)):
    temp = crud.getTemplate_by_id(db, template_id=template_id)
    # print(temp.name)
    if temp:
        r = crud.editTemplate(db, template_id=template_id, template=template)
        if r:
            return {'type': 'success', 'msg': '编辑成功'}
        else:
            return {'type': 'error', 'msg': '编辑失败'}
    else:
        return {'type': 'error', 'msg': '模板不存在'}


@router.post("/")
async def createTemplate(template: schemas.TemplateCreate, db: Session = Depends(get_db)):
    temp = crud.getTemplate_by_name(db, template_name=template.name)
    if temp:
        # raise HTTPException(status_code=400, detail="The template name already exists")
        return {'type': 'error', 'msg': '增加失败,已存在'}
    else:
        crud.createTemplate(db, template=template)
        # return t
        return {'type': 'success', 'msg': '增加成功'}


@router.delete("/{template_id}")
async def deleteTemplate(template_id: int, db: Session = Depends(get_db)):
    temp = crud.getTemplate_by_id(db, template_id=template_id)
    if temp:
        crud.deleteTemplate(db, template_id=template_id)
        return {'type': 'success', 'msg': '删除成功'}
    else:
        return {'type': 'error', 'msg': '删除失败，数据不存在'}

