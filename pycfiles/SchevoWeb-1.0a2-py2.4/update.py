# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/schevoweb/form/update.py
# Compiled at: 2006-09-08 16:55:59
"""Update fieldspaces.

For copyright, license, and warranty, see bottom of file.
"""
import dispatch
from schevo import base
from schevo.constant import UNASSIGNED
from schevo import query

@dispatch.generic()
def update(db, obj, kw, prefix='', **options):
    """Update a Schevo object's fields using keywords.

    - ``db``: The Schevo database being used.

    - ``obj``: The object whose fields will be updated.
    
    - ``kw``: Dictionary of {key: string-value} pairs, usually from
      HTTP POST data.

    - ``prefix``: The prefix that key names start with in ``kw``.

    Returns a dictionary containing {key: (message, exception)} items
    representing errors occurring during the update.
    """
    pass


@update.when('isinstance(obj, query.Intersection)')
def update_intersection(db, obj, kw, prefix='', **options):
    errors = {}
    index = 0
    for subquery in obj.queries:
        sub_kw = kw.get(str(index), {})
        errors.update(update(db, subquery, sub_kw, prefix, **options))
        index += 1

    return errors


@update.when('isinstance(obj, query.Match)')
def update_match(db, obj, kw, prefix='', **options):
    operator_name = kw.get('operator', None)
    if operator_name:
        obj.operator = operator_name
    value = kw.get('value', '')
    field = obj.FieldClass(obj, 'value')
    field.assign(value)
    obj.value = field.get()
    return {}


@update.when('isinstance(obj, base.classes_using_fields)')
def update_fields(db, obj, kw, prefix='', **options):
    """Additional options:

    - ``update_unassigned``: Update fields to UNASSIGNED of an
      _unassigned_fieldname value is found.

    - ``update_assigned``: Update fields' assigned status based on
      existence of _assigned_fieldname values.
    """
    f = obj.f
    errors = {}
    update_unassigned = options.get('update_unassigned', False)
    update_assigned = options.get('update_assigned', False)
    for name in f:
        field = f[name]
        if field.readonly:
            continue
        if prefix:
            kw_name = prefix + name
            unassigned_kw_name = prefix + '_unassigned_' + name
            assigned_kw_name = prefix + '_assigned_' + name
        else:
            kw_name = name
            unassigned_kw_name = '_unassigned_' + name
            assigned_kw_name = '_assigned_' + name
        if kw_name in kw:
            value = kw[kw_name]
        elif field.required:
            value = UNASSIGNED
        else:
            value = None
        if update_unassigned and kw.get(unassigned_kw_name, False):
            value = UNASSIGNED
        if value is not None:
            try:
                value = field.convert(value, db)
                field.verify(value)
                setattr(obj, name, value)
            except (AttributeError, ValueError, TypeError), e:
                errors[name] = (
                 e.args[0], e)

        if update_assigned:
            field.assigned = bool(kw.get(assigned_kw_name, False))

    return errors