# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/object.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the base Object class for taurus."""
from builtins import object
__all__ = [
 'Object']
__docformat__ = 'restructuredtext'

class Object(object):

    def __init__(self):
        pass

    def call__init__(self, klass, *args, **kw):
        """Method to be called from subclasses to call superclass corresponding
        __init__ method. This method ensures that classes from diamond like
        class hierarquies don't call their super classes __init__ more than
        once."""
        if 'inited_class_list' not in self.__dict__:
            self.inited_class_list = []
        if klass not in self.inited_class_list:
            self.inited_class_list.append(klass)
            klass.__init__(self, *args, **kw)

    def call__init__wo_kw(self, klass, *args):
        """Same as call__init__ but without keyword arguments because PyQT does
        not support them."""
        if 'inited_class_list' not in self.__dict__:
            self.inited_class_list = []
        if klass not in self.inited_class_list:
            self.inited_class_list.append(klass)
            klass.__init__(self, *args)

    def getAttrDict(self):
        attr = dict(self.__dict__)
        if 'inited_class_list' in attr:
            del attr['inited_class_list']
        return attr

    def updateAttrDict(self, other):
        attr = other.getAttrDict()
        self.__dict__.update(attr)