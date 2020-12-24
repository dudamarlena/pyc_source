# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_permissions/licences.py
# Compiled at: 2019-10-27 21:48:09
# Size of source mod 2**32: 1615 bytes


def create(user, collection=None, **kwargs):
    if collection is None:
        return False
    else:
        return user.is_authenticated or False
    if user.is_superuser:
        return True
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)


def list(user, collection=None, **kwargs):
    if collection is None:
        return False
    else:
        return user.is_authenticated or False
    if user.is_special:
        return True
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)


def view(user, licence=None, **kwargs):
    if licence is None:
        return False
    else:
        return user.is_authenticated or False
    if user.is_special:
        return True
    collection = licence.collection
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)


def change(user, licence=None, **kwargs):
    if licence is None:
        return False
    else:
        return user.is_authenticated or False
    if user.is_superuser:
        return True
    collection = licence.collection
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)


def delete(user, licence=None, **kwargs):
    if licence is None:
        return False
    else:
        return user.is_authenticated or False
    if user.is_superuser:
        return True
    collection = licence.collection
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)