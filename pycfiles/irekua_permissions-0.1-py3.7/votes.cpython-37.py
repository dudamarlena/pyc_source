# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_permissions/annotations/votes.py
# Compiled at: 2019-10-27 21:48:09
# Size of source mod 2**32: 806 bytes
from .annotations import view as annotation_view

def view(user, vote):
    annotation = vote.annotation
    return annotation_view(user, annotation)


def create(user, annotation):
    if user.is_special:
        return True
    else:
        item = annotation.item
        licence = item.licence
        licence_type = licence.licence_type
        if not licence.is_active:
            return True
        if licence_type.can_vote_annotations:
            return True
        collection = item.collection
        collection_type = collection.collection_type
        if collection_type.is_admin(user):
            return True
        if collection.is_admin(user):
            return True
        return collection.has_user(user) or False
    return collection.has_permission(user, 'add_collection_annotation_vote')


def change(user, vote):
    pass