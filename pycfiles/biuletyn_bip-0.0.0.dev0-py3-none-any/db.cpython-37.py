# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/db.py
# Compiled at: 2019-09-03 15:15:23
# Size of source mod 2**32: 239 bytes
import flask_sqlalchemy.model as BaseModel

class MappedModelMixin:
    __mapper_args__ = {'confirm_deleted_rows': False}


class Model(BaseModel, MappedModelMixin):

    def get_id(self):
        return self.pk