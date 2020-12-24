# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/label.py
# Compiled at: 2007-03-21 14:34:41
"""Schevo object decoration.

For copyright, license, and warranty, see bottom of file.
"""
import re, sys
from schevo.lib import optimize

class LabelMixin(object):
    """Mix this in with classes that have labels themselves via a
    `_label` attribute, and whose instances have labels via a
    `__str__` method.

    Example: Entity.
    """
    __module__ = __name__
    __slots__ = []


def label(obj):
    """Return the unicode label for `obj`.

    In the case of nouns, return the singular label.

    In the case of verbs, return the present tense form.
    """
    if isinstance(obj, LabelMixin):
        return unicode(obj)
    elif hasattr(obj, '_label'):
        return unicode(obj._label)
    elif hasattr(obj, 'label'):
        return unicode(obj.label)
    else:
        return unicode(obj)


def plural(obj):
    """Return the plural noun label for `obj`."""
    if hasattr(obj, '_plural'):
        return unicode(obj._plural)


def label_from_name(name):
    """Return a label based on the given object name."""
    parts = [ part for part in name.split('_') if part ]
    if len(parts) > 1:
        parts = (part[0].upper() + part[1:] for part in parts if part)
        name = (' ').join(parts)
    else:
        name = parts[0]
        name = name[0].upper() + name[1:]
        rawstr = '([A-Z][a-z]*)'
        compile_obj = re.compile(rawstr)
        parts = compile_obj.split(name)
        name = (' ').join((part for part in parts if part))
    return unicode(name)


def plural_from_name(name):
    """Return a plural label based on the given object name."""
    return label_from_name(name) + 's'


def with_label(label, plural=None):
    """Return a decorator that assigns a label and an optional plural
    label to a function."""

    def label_decorator(fn):
        fn._label = unicode(label)
        if plural is not None:
            fn._plural = unicode(plural)
        return fn

    return label_decorator


optimize.bind_all(sys.modules[__name__])