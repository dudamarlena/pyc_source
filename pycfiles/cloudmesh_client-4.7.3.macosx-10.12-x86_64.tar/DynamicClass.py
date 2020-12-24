# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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