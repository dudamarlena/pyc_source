# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/db/declarative.py
# Compiled at: 2012-10-19 18:33:24
""" store the declarative_base in this module
"""
from sqlalchemy.ext.declarative import declarative_base

class ORMClass(object):

    @classmethod
    def query(cls):
        from oyProjectManager.db import query
        return query(cls)


Base = declarative_base(cls=ORMClass)