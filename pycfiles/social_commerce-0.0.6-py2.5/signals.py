# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/mptt/signals.py
# Compiled at: 2009-10-31 23:19:40
"""
Signal receiving functions which handle Modified Preorder Tree Traversal
related logic when model instances are about to be saved or deleted.
"""
import operator
from django.db.models.query import Q
__all__ = ('pre_save', )

def _insertion_target_filters(node, order_insertion_by):
    """
    Creates a filter which matches suitable right siblings for ``node``,
    where insertion should maintain ordering according to the list of
    fields in ``order_insertion_by``.

    For example, given an ``order_insertion_by`` of
    ``['field1', 'field2', 'field3']``, the resulting filter should
    correspond to the following SQL::

       field1 > %s
       OR (field1 = %s AND field2 > %s)
       OR (field1 = %s AND field2 = %s AND field3 > %s)

    """
    fields = []
    filters = []
    for field in order_insertion_by:
        value = getattr(node, field)
        filters.append(reduce(operator.and_, [ Q(**{f: v}) for (f, v) in fields ] + [
         Q(**{'%s__gt' % field: value})]))
        fields.append((field, value))

    return reduce(operator.or_, filters)


def _get_ordered_insertion_target(node, parent):
    """
    Attempts to retrieve a suitable right sibling for ``node``
    underneath ``parent`` (which may be ``None`` in the case of root
    nodes) so that ordering by the fields specified by the node's class'
    ``order_insertion_by`` option is maintained.

    Returns ``None`` if no suitable sibling can be found.
    """
    right_sibling = None
    if parent is None or parent.get_descendant_count() > 0:
        opts = node._meta
        order_by = opts.order_insertion_by[:]
        filters = _insertion_target_filters(node, order_by)
        if parent:
            filters = filters & Q(**{opts.parent_attr: parent})
            order_by.append(opts.left_attr)
        else:
            filters = filters & Q(**{'%s__isnull' % opts.parent_attr: True})
            order_by.append(opts.tree_id_attr)
        try:
            right_sibling = node._default_manager.filter(filters).order_by(*order_by)[0]
        except IndexError:
            pass

    return right_sibling


def pre_save(instance, **kwargs):
    """
    If this is a new node, sets tree fields up before it is inserted
    into the database, making room in the tree structure as neccessary,
    defaulting to making the new node the last child of its parent.

    It the node's left and right edge indicators already been set, we
    take this as indication that the node has already been set up for
    insertion, so its tree fields are left untouched.

    If this is an existing node and its parent has been changed,
    performs reparenting in the tree structure, defaulting to making the
    node the last child of its new parent.

    In either case, if the node's class has its ``order_insertion_by``
    tree option set, the node will be inserted or moved to the
    appropriate position to maintain ordering by the specified field.
    """
    if kwargs.get('raw'):
        return
    opts = instance._meta
    parent = getattr(instance, opts.parent_attr)
    if not instance.pk:
        if getattr(instance, opts.left_attr) and getattr(instance, opts.right_attr):
            return
        if opts.order_insertion_by:
            right_sibling = _get_ordered_insertion_target(instance, parent)
            if right_sibling:
                instance.insert_at(right_sibling, 'left')
                return
        instance.insert_at(parent, position='last-child')
    else:
        old_parent = getattr(instance._default_manager.get(pk=instance.pk), opts.parent_attr)
        if parent != old_parent:
            setattr(instance, opts.parent_attr, old_parent)
            try:
                if opts.order_insertion_by:
                    right_sibling = _get_ordered_insertion_target(instance, parent)
                    if right_sibling:
                        instance.move_to(right_sibling, 'left')
                        return
                instance.move_to(parent, position='last-child')
            finally:
                setattr(instance, opts.parent_attr, parent)