# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\procode\login_init\model_interface.py
# Compiled at: 2019-09-03 08:04:22
# Size of source mod 2**32: 410 bytes
__doc__ = '\nauthor:hexiaoxia\ndate:2019/09/03\n与model层通信接口\n'
from poslocalmodel.pos_sys.pos_global_obj import PosGlobalObj

class ModelInterface(object):

    def __init__(self):
        pass

    def getparam_checkcpu(self):
        cpu = PosGlobalObj.Cpuserialnumber
        return {'CPU': cpu}


class_dict = {key:var for key, var in locals().items() if isinstance(var, type) if isinstance(var, type)}