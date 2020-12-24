# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_permissions/devices/physical_devices.py
# Compiled at: 2019-10-27 21:48:09
# Size of source mod 2**32: 728 bytes


def view(user, physical_device=None, **kwargs):
    if physical_device is None:
        return False
    else:
        return user.is_authenticated or False
    if user.is_special:
        return True
    return physical_device.created_by == user


def create(user, **kwargs):
    return user.is_authenticated


def change(user, physical_device=None, **kwargs):
    if physical_device is None:
        return False
    else:
        return user.is_authenticated or False
    return physical_device.created_by == user


def delete(user, physical_device=None, **kwargs):
    if physical_device is None:
        return False
    else:
        return user.is_authenticated or False
    return physical_device.created_by == user