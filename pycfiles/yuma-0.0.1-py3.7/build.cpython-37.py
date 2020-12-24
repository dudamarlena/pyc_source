# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\yuma\mysql\build.py
# Compiled at: 2020-01-15 21:45:05
# Size of source mod 2**32: 1786 bytes
from mysqlmapper.mysql.mvc.holder import MVCHolder
from yuma.model import Permission, PermissionGroup
from yuma.permission import PermissionHolder

def get_permission_holder(mvc_holder: MVCHolder):
    """
    Get permission holder from mysql
    :param mvc_holder: MVCHolder
    :return: PermissionHolder
    """
    holder = PermissionHolder()
    _get_permissions(holder, mvc_holder)
    _get_group(holder, mvc_holder)
    return holder.build_tree()


def _get_permissions(holder: PermissionHolder, mvc_holder: MVCHolder):
    """
    Get permissions from mysql
    :param holder: PermissionHolder
    :param mvc_holder: MVCHolder
    """
    yuma_permission_service = mvc_holder.services['yuma_permission']
    data = yuma_permission_service.get_list({'Start': -1})
    for item in data:
        holder.add_permission(Permission(item['id'], item['permission_key'], item['memo'], item['father_id']))


def _get_group(holder: PermissionHolder, mvc_holder: MVCHolder):
    """
    Get group from mysql
    :param holder: PermissionHolder
    :param mvc_holder: MVCHolder
    """
    yuma_group_service = mvc_holder.services['yuma_group']
    yuma_group_permission_service = mvc_holder.services['yuma_group_permission']
    group_list = yuma_group_service.get_list({'Start': -1})
    for group in group_list:
        key = group['group_key']
        permission_group = PermissionGroup(key)
        permission_list = yuma_group_permission_service.get_list({'group_key':key,  'Start':-1})
        for permission in permission_list:
            permission_group.add_id(permission['permission_id'])

        holder.add_permission_group(permission_group)