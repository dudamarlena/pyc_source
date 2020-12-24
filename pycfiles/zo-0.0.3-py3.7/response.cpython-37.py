# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/fastapi/response.py
# Compiled at: 2020-04-03 02:02:22
# Size of source mod 2**32: 595 bytes
from typing import *
from zo.pydantic import BaseModel, EmailStr, HttpUrl, validator, constr

class RespBase(BaseModel):
    message = 'ok'
    message: str
    result: Any
    detail = {}
    detail: dict


class RespDict(RespBase):
    result: dict


class RespList(RespBase):
    result: List


class RespStr(RespBase):
    result: str


class RespInt(RespBase):
    result: int


class RespFloat(RespBase):
    result: float


def resp(result=None, **kwargs) -> RespBase:
    return RespBase(result=({} if result is None else result), detail=kwargs)