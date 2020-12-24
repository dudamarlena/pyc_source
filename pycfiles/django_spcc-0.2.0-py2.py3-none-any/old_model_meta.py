# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\SM\CODE\django-aops-sunteng\aops\libs\models\old_model_meta.py
# Compiled at: 2018-03-05 02:17:05
"""
升级至Django 1.11，部分api被去除。
以下是根据官方文档给出的替代方法
https://docs.djangoproject.com/en/1.11/ref/models/meta/
"""

def get_fields_with_model(model=None):
    fields = []
    if model:
        fields = [ (f, f.model if f.model != model else None) for f in model._meta.get_fields() if not f.is_relation or f.one_to_one or f.many_to_one and f.related_model
                 ]
    return fields


def get_concrete_fields_with_model(model=None):
    fields = []
    if model:
        fields = [ (f, f.model if f.model != model else None) for f in model._meta.get_fields() if f.concrete and (not f.is_relation or f.one_to_one or f.many_to_one and f.related_model)
                 ]
    return fields


def get_m2m_with_model(model=None):
    fields = []
    if model:
        fields = [ (f, f.model if f.model != model else None) for f in model._meta.get_fields() if f.many_to_many and not f.auto_created
                 ]
    return fields


def get_all_related_objects(model=None):
    fields = []
    if model:
        fields = [ f for f in model._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
                 ]
    return fields


def get_all_related_objects_with_model(model=None):
    fields = []
    if model:
        fields = [ (f, f.model if f.model != model else None) for f in model._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
                 ]
    return fields


def get_all_related_many_to_many_objects(model=None):
    fields = []
    if model:
        fields = [ f for f in model._meta.get_fields(include_hidden=True) if f.many_to_many and f.auto_created
                 ]
    return fields


def get_all_related_m2m_objects_with_model(model=None):
    fields = []
    if model:
        fields = [ (f, f.model if f.model != model else None) for f in model._meta.get_fields(include_hidden=True) if f.many_to_many and f.auto_created
                 ]
    return fields


def get_all_field_names(model=None):
    from itertools import chain
    fields = []
    if model:
        fields = list(set(chain.from_iterable(((field.name, field.attname) if hasattr(field, 'attname') else (field.name,)) for field in model._meta.get_fields() if not (field.many_to_one and field.related_model is None))))
    return fields


def get_all_field_names2(model=None):
    fields = []
    if model:
        fields = [ f.name for f in model._meta.get_fields() ]
    return fields