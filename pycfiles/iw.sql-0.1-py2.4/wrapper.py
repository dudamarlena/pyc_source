# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/sql/wrapper.py
# Compiled at: 2007-12-17 11:25:35
"""
This module contains a base wrapper for SQL connections
"""
from z3c.sqlalchemy.base import BaseWrapper
import sqlalchemy

def retry_on_failure(func):
    """retry-on-failure decorator"""

    def _w_retry_on_failure(*args, **kw):
        try:
            return func(*args, **kw)
        except:
            return func(*args, **kw)

    return _w_retry_on_failure


def _secured_query(query):
    """returned a query object which methods are decorated"""

    def _w_secured_query(*args, **kw):
        query_object = query(*args, **kw)
        return DynamicDecorator(query_object, retry_on_failure)

    return _w_secured_query


class DynamicDecorator(object):
    """will dynamically decorate a class"""
    __module__ = __name__

    def __init__(self, instance, decorator, method_name=None):
        self.__instance = instance
        self.__method = method_name
        self.__decorator = decorator

    def __getattr__(self, name):
        if hasattr(self.__instance, name):
            attr = getattr(self.__instance, name)
            if type(attr).__name__ == 'instancemethod':
                if self.__method is None or attr.im_func.func_name == self.__method:
                    return self.__decorator(attr)
            return attr
        raise AttributeError(name)
        return


def _secured_session(engine):
    """returns a decorated session object
    when `query` is invoqued, it's done through `_secured_query`
    """
    return DynamicDecorator(sqlalchemy.create_session(engine), _secured_query, 'query')


class SecuredBaseWrapper(BaseWrapper):
    """overrides the base wrapper to provide retry-on-failure
    pattern"""
    __module__ = __name__

    @property
    def session(self):
        return _secured_session(self._engine)