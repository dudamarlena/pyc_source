# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\login_init\model_interface.py
# Compiled at: 2019-09-03 08:04:22
# Size of source mod 2**32: 410 bytes
"""
author:hexiaoxia
date:2019/09/03
与model层通信接口
"""
from poslocalmodel.pos_sys.pos_global_obj import PosGlobalObj

class ModelInterface(object):

    def __init__(self):
        pass

    def getparam_checkcpu(self):
        cpu = PosGlobalObj.Cpuserialnumber
        return {'CPU': cpu}


class_dict = {key:var for key, var in locals().items() if isinstance(var, type) if isinstance(var, type)}