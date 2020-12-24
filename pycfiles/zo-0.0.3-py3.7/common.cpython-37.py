# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/fastapi/common.py
# Compiled at: 2020-04-02 19:59:37
# Size of source mod 2**32: 664 bytes
import time
from fastapi import Query
from .model import PageArgs
from .error import abort_if
from ..aa import timestamp_int
from ..db import conn_db

async def common_page_args(q: str=None, page: int=Query(1, ge=1, le=1000), page_size: int=Query(10, description='range: 1~100', ge=1, le=100)):
    return PageArgs(q=q, page=page, page_size=page_size)


async def check_reset_key(key: int=0):
    abort_if(abs(time.time() - key) > 60, f"reset_key_error: valid key = {timestamp_int() + 60}")


async def get_new_id(key, name='id', decimals=8):
    db = conn_db()
    return str(db.zincr(name, key, decimals=decimals))