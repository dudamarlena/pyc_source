# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/sql/models.py
# Compiled at: 2015-04-19 06:32:47
# Size of source mod 2**32: 593 bytes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from hatak.unpackrequest import unpack
DeclatativeBase = declarative_base()

class Base(AbstractConcreteBase, DeclatativeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    def assign_request(self, request):
        self.request = request
        unpack(self, request)

    def __repr__(self):
        id_ = str(self.id) if self.id else 'None'
        return '%s (%s)' % (self.__class__.__name__, id_)