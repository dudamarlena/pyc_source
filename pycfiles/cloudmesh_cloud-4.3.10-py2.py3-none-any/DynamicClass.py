# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/DynamicClass.py
# Compiled at: 2017-04-23 10:30:41
import importlib

class DynamicClass(object):

    def add_instance_method(self, f):
        setattr(self, f.__name__, f)

    @classmethod
    def add_classmethod(cls, f):
        setattr(cls, f.__name__, f)

    def load_instancemethod(self, location):
        module_name, class_name = location.rsplit('.', 1)
        f = getattr(importlib.import_module(module_name), class_name)
        self.add_instance_method(f)

    @classmethod
    def load_classmethod(cls, location):
        module_name, class_name = location.rsplit('.', 1)
        f = getattr(importlib.import_module(module_name), class_name)
        cls.add_classmethod(f)