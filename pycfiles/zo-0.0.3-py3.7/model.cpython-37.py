# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/pydantic/model.py
# Compiled at: 2020-04-01 05:10:57
# Size of source mod 2**32: 257 bytes
from pydantic import BaseModel

class BaseModelValidation(BaseModel):

    class Config:
        validate_assignment = True


class BaseModelWithoutValidation(BaseModel):

    class Config:
        validate_assignment = False