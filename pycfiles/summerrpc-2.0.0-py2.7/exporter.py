# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/exporter.py
# Compiled at: 2018-07-31 10:42:31
"""
exporter：导入要暴漏的方法
"""
__all__ = [
 'Exporter']
__authors__ = ['Tim Chow']
import inspect, warnings
from .decorator import get_export, get_provide
from .heartbeat import HeartBeatRequest

class Exporter(object):

    def __init__(self, install_hearbeat=True):
        self._exporters = {}
        self._class_name_to_object = {}
        if install_hearbeat:
            self.export(HeartBeatRequest)

    def export(self, cls, cover=False):
        if not inspect.isclass(cls):
            warnings.warn('expect class, not %s' % type(cls).__name__, RuntimeWarning)
            return self
        else:
            export = get_export(cls)
            if export is None:
                class_name = getattr(cls, '__name__')
            else:
                class_name = export['name']
            if class_name in self._exporters and not cover:
                warnings.warn('%s alreay exists' % repr(cls), RuntimeWarning)
                return self
            d = self._exporters[class_name] = {}
            instance = cls()
            self._class_name_to_object[class_name] = instance
            for attr_name, attr_value in vars(cls).iteritems():
                if not inspect.isfunction(attr_value) and not inspect.ismethod(attr_value):
                    continue
                if attr_name.startswith('_'):
                    continue
                provide = get_provide(attr_value)
                if provide is not None:
                    if provide['filtered']:
                        continue
                    d[provide['name']] = getattr(instance, attr_name)
                else:
                    d[attr_name] = getattr(instance, attr_name)

            return self

    def get_method(self, class_name, method_name):
        return self._exporters.get(class_name, {}).get(method_name)

    def iter_method(self):
        for class_name, name_to_method in self._exporters.iteritems():
            for method_name, method in name_to_method.iteritems():
                yield (
                 class_name, method_name, method)

    def get_object(self, class_name):
        return self._class_name_to_object.get(class_name)