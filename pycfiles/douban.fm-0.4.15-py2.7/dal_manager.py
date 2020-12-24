# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/dal/dal_manager.py
# Compiled at: 2016-06-22 17:23:26
from doubanfm.dal.dal_main import MainDal
from doubanfm.colorset.colors import color_func

class ManagerDal(MainDal):

    def __init__(self, data):
        super(ManagerDal, self).__init__(data)