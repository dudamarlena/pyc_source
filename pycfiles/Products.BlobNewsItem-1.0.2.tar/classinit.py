# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/classinit.py
# Compiled at: 2012-02-27 07:41:58


class ClassInitMeta(type):

    def __new__(meta, class_name, bases, new_attrs):
        cls = type.__new__(meta, class_name, bases, new_attrs)
        if new_attrs.has_key('__classinit__') and not isinstance(cls.__classinit__, staticmethod):
            setattr(cls, '__classinit__', staticmethod(cls.__classinit__.im_func))
        if hasattr(cls, '__classinit__'):
            cls.__classinit__(cls, new_attrs)
        return cls


def build_properties(cls, new_attrs):
    """
    Given a class and a new set of attributes (as passed in by
    __classinit__), create or modify properties based on functions
    with special names ending in __get, __set, and __del.
    """
    for (name, value) in new_attrs.items():
        if name.endswith('__get') or name.endswith('__set') or name.endswith('__del'):
            base = name[:-5]
            if hasattr(cls, base):
                old_prop = getattr(cls, base)
                if not isinstance(old_prop, property):
                    raise ValueError('Attribute %s is a %s, not a property; function %s is named like a property' % (
                     base, type(old_prop), name))
                attrs = {'fget': old_prop.fget, 'fset': old_prop.fset, 'fdel': old_prop.fdel, 
                   'doc': old_prop.__doc__}
            else:
                attrs = {}
            attrs['f' + name[-3:]] = value
            if name.endswith('__get') and value.__doc__:
                attrs['doc'] = value.__doc__
            new_prop = property(**attrs)
            setattr(cls, base, new_prop)