# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/application_context.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'ApplicationContext',
 'BasePackageApplicationContext',
 'FilePathApplicationContext']
__authors__ = ['Tim Chow']
from .bean import *
from .exception import *
from .bean_factory import BeanFactory

class ApplicationContext(BeanFactory):

    def __init__(self, bean_classes):
        BeanFactory.__init__(self, bean_classes)
        for name in self._name_to_bean:
            bean = self._name_to_bean[name]
            if bean.is_singleton:
                self.get_bean(bean.name)

    def add_bean(self, bean_class, mod=None):
        if not is_bean_class(bean_class, mod):
            raise UnavaliableBeanClassError
        bean = Bean.from_bean_class(bean_class)
        if bean.name in self._name_to_bean:
            raise DuplicateBeanNameError
        self._name_to_bean[bean.name] = bean
        if bean.is_singleton:
            self.get_bean(bean.name)

    def close(self):
        self.destroy()

    def __del__(self):
        try:
            self.close()
        except AttributeError:
            pass


class BasePackageApplicationContext(ApplicationContext):

    def __init__(self, *packages):
        ApplicationContext.__init__(self, component_scan_package(*packages))


class FilePathApplicationContext(ApplicationContext):

    def __init__(self, *paths):
        ApplicationContext.__init__(self, component_scan_path(*paths))