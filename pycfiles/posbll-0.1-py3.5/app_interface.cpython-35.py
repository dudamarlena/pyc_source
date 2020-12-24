# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\posbll\app_interface.py
# Compiled at: 2019-09-04 23:27:19
# Size of source mod 2**32: 3932 bytes
"""
author:hexiaoxia
date:2019/08/21
app与bll层通信接口类
"""
from poslocalmodel.enums.public_enums import *
from poslocalmodel.pos_sys.posnowinfo import *
import importlib

class AppInterface(object):
    _AppInterface__businessnode = None

    def __init__(self, module, funname, offoronline=OffOrOnLineEnum.offandon):
        self._AppInterface__module = module
        self._AppInterface__funname = funname
        self._AppInterface__isonline = offoronline

    def set_businessnode(self, busnode):
        self._AppInterface__businessnode = busnode

    def get_module(self):
        return self._AppInterface__module

    def get_funname(self):
        return self._AppInterface__funname

    def get_busnode(self):
        return self._AppInterface__busnode

    def get_isonline(self):
        return self._AppInterface__isonline

    def execute_route_fun(self, **kwargs):
        """
        前端路由调用的具体业务接口方法实现
        :param kwargs:
        :return:
        """
        print(kwargs)
        if self._AppInterface__businessnode != None and self._AppInterface__businessnode == kwargs.get('busnode', None):
            return
        if self.get_isonline() == OffOrOnLineEnum.offandon:
            res = self._onlinefun(**kwargs)
            if res.get('code', -1) != 0:
                res = self._offlinefun(**kwargs)
                return res
            else:
                return res
        else:
            if self.get_isonline() == OffOrOnLineEnum.offline:
                res = self._offlinefun(**kwargs)
                return res
            else:
                res = self._onlinefun(**kwargs)
                return res

    def _onlinefun(self, **kwargs):
        res = {'code': -1, 'message': ''}
        if PosNowInfo.Serverapi == 0:
            class_name = 'OnLineClass'
            module_name = 'online'
            method = self.get_funname()
            module = 'procode.' + self.get_module() + '.' + module_name
            module = importlib.import_module(module)
            c = getattr(module, class_name)
            obj = c(self.get_module())
            mtd = getattr(obj, method)
            res = mtd(**kwargs)
        else:
            res['code'] = -2
            res['message'] = '网络不通，无法使用在线功能'
        return res

    def _offlinefun(self, **kwargs):
        class_name = 'OffLineClass'
        module_name = 'offline'
        method = self.get_funname()
        module = 'procode.' + self.get_module() + '.' + module_name
        module = importlib.import_module(module)
        c = getattr(module, class_name)
        obj = c()
        mtd = getattr(obj, method)
        res = mtd(**kwargs)
        return res

    def execute_app_fun(self, module_name):
        """
        非路由的，客户端python自身业务方法需要app层与其它层通信时模块对象获取
        :param module_name:
        :return:
        """
        class_name = ''
        modulepath = 'procode.' + self.get_module() + '.' + module_name
        try:
            module = importlib.import_module(modulepath)
            cc = getattr(module, 'class_dict')
            for k, v in cc.items():
                if modulepath in str(cc[k]):
                    class_name = str(k)
                    break

            c = getattr(module, class_name)
            return c
        except Exception as e:
            return

    def __str__(self):
        return str(self.__dict__)