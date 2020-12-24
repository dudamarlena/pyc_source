# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/meta.py
# Compiled at: 2007-03-21 14:34:41
"""Metaclasses.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo.fieldspec import field_spec_from_class
from schevo.label import label_from_name
import schevo.namespace

def schema_metaclass(namespace_name):
    """Return a metaclass that adds subclasses to a namespace of a
    SchemaDefinition."""

    class Meta(type):
        __module__ = __name__

        def __init__(cls, class_name, bases, class_dict):
            type.__init__(cls, class_name, bases, class_dict)
            if '_label' not in class_dict:
                cls._label = label_from_name(class_name)
            if schevo.namespace.SCHEMADEF is not None and hasattr(cls, '_field_spec'):
                cls._field_spec = field_spec_from_class(cls, class_dict)
                ns = getattr(schevo.namespace.SCHEMADEF, namespace_name)
                try:
                    ns._set(class_name, cls)
                except KeyError:
                    pass

            return

    return Meta


optimize.bind_all(sys.modules[__name__])