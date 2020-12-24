# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_permissions/data_collections/data_collections.py
# Compiled at: 2019-10-27 21:48:09
# Size of source mod 2**32: 983 bytes


def view(user, collection=None, **kwargs):
    if collection.is_open:
        return True
    else:
        return user.is_authenticated or False
    if user.is_special:
        return True
    if collection.collection_type.is_admin(user):
        return True
    if collection.is_admin(user):
        return True
    return collection.is_user(user)


def create(user, collection_type=None, **kwargs):
    if not user.is_authenticated:
        return False
    return collection_type.is_admin(user)


def change(user, collection=None, **kwargs):
    if not user.is_authenticated:
        return False
    if user.is_superuser | user.is_curator:
        return True
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)


def delete(user, collection=None, **kwargs):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return collection.collection_type.is_admin(user)