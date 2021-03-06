# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_permissions/sampling_events/sampling_events.py
# Compiled at: 2019-10-27 21:48:09
# Size of source mod 2**32: 2571 bytes


def view(user, sampling_event=None, **kwargs):
    if sampling_event is None:
        return False
    else:
        collection = sampling_event.collection
        if collection.is_open:
            return True
        if not user.is_authenticated:
            return False
        if sampling_event.created_by == user:
            return True
        if user.is_special:
            return True
        if collection.collection_type.is_admin(user):
            return True
        if collection.is_admin(user):
            return True
        return collection.is_user(user) or False
    role = collection.get_user_role(user)
    return role.has_permission('view_collection_sampling_events')


def list(user, collection=None, **kwargs):
    if collection is None:
        return False
    else:
        return user.is_authenticated or False
    if collection.is_open:
        return True
    if user.is_special:
        return True
    if collection.collection_type.is_admin(user):
        return True
    if collection.is_admin(user):
        return True
    return collection.is_user(user)


def create(user, collection=None, **kwargs):
    if collection is None:
        return False
    else:
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if collection.collection_type.is_admin(user):
            return True
        if collection.is_admin(user):
            return True
        return collection.is_user(user) or False
    role = collection.get_user_role(user)
    return role.has_permission('add_collection_sampling_event')


def change(user, sampling_event=None, **kwargs):
    if sampling_event is None:
        return False
    else:
        if not user.is_authenticated:
            return False
        if sampling_event.created_by == user:
            return True
        if user.is_superuser:
            return True
        collection = sampling_event.collection
        if collection.collection_type.is_admin(user):
            return True
        if collection.is_admin(user):
            return True
        return collection.is_user(user) or False
    role = collection.get_user_role(user)
    return role.has_permission('change_collection_sampling_event')


def delete(user, sampling_event=None, **kwargs):
    if sampling_event is None:
        return False
    else:
        return user.is_authenticated or False
    if sampling_event.created_by == user:
        return True
    if user.is_superuser:
        return True
    collection = sampling_event.collection
    if collection.collection_type.is_admin(user):
        return True
    return collection.is_admin(user)