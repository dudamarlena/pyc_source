# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_permissions/sites.py
# Compiled at: 2019-10-27 21:48:09
# Size of source mod 2**32: 584 bytes


def view(user, site=None, **kwargs):
    if site is None:
        return False
    else:
        return user.is_authenticated or False
    return site.created_by == user


def create(user, **kwargs):
    return user.is_authenticated


def change(user, site=None, **kwargs):
    if site is None:
        return False
    else:
        return user.is_authenticated or False
    return site.created_by == user


def delete(user, site=None, **kwargs):
    if site is None:
        return False
    else:
        return user.is_authenticated or False
    return site.created_by == user