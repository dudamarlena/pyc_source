# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\blltoapp_interface.py
# Compiled at: 2019-09-04 05:27:09
# Size of source mod 2**32: 1564 bytes
"""
author:hexiaoxia
date:2019/08/21
bll层调用app层的调用js方法模块接口类
"""
import importlib

class BllToAppInterface(object):

    def __init__(self, module, funname):
        self._BllToAppInterface__module = module
        self._BllToAppInterface__funname = funname

    def get_module(self):
        return self._BllToAppInterface__module

    def get_funname(self):
        return self._BllToAppInterface__funname

    def executefun(self, jsonparam):
        """
        bll调用前端js
        :param kwargs:
        :return:
        """
        method = self.get_funname()
        module = 'poswebapp.bll_to_app_function.' + self.get_module()
        module = importlib.import_module(module)
        fun = None
        for name in dir(module):
            attr = getattr(module, name)
            if hasattr(attr, '__module__') and attr.__module__ == module.__name__:
                fun = attr
                break

        fun(jsonparam)

    def __str__(self):
        return str(self.__dict__)