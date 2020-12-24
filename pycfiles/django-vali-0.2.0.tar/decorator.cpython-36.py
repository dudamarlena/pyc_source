# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/anyi/workspace/svn/xunjian_admin/vali/decorator.py
# Compiled at: 2018-06-22 02:44:50
# Size of source mod 2**32: 408 bytes
from django.contrib import admin

def vali_models_group(groupname=''):
    """
    assign menu_group name to ModalAdmin instance,
    admin index display registered models group by menu_group
    :param groupname:
    :return:
    """

    def _models_group(cls):
        if issubclass(cls, admin.ModelAdmin):
            if groupname:
                cls.model_group = groupname
        return cls

    return _models_group