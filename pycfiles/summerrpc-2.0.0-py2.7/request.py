# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/request.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Request']
__authors__ = ['Tim Chow']
from .exception import RequestValidateError

class Request(object):

    def __init__(self):
        self._class_name = None
        self._method_name = None
        self._args = tuple()
        self._kwargs = dict()
        self._meta = None
        return

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, class_name):
        self._class_name = class_name

    @property
    def method_name(self):
        return self._method_name

    @method_name.setter
    def method_name(self, method_name):
        self._method_name = method_name

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, meta):
        self._meta = meta

    def validate(self):
        if self.class_name is None or self.method_name is None:
            raise RequestValidateError('missing class name or method name')
        return