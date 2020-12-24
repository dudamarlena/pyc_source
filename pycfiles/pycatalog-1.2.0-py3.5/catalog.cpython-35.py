# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catalog.py
# Compiled at: 2017-09-01 15:08:32
# Size of source mod 2**32: 4850 bytes
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
import sys, inspect
from collections import OrderedDict
from functools import wraps
from itertools import zip_longest
from future.utils import with_metaclass

class Prepareable(type):
    if sys.version_info < (3, ):

        def __new__(cls, name, bases, attributes):
            try:
                constructor = attributes['__new__']
            except KeyError:
                return type.__new__(cls, name, bases, attributes)

            def preparing_constructor(cls, name, bases, attributes):
                try:
                    cls.__prepare__
                except AttributeError:
                    return constructor(cls, name, bases, attributes)

                namespace = cls.__prepare__.im_func(cls, name, bases)
                defining_frame = sys._getframe(1)

                def get_index(*args, **kwargs):
                    return 0

                for constant in reversed(defining_frame.f_code.co_consts):
                    if inspect.iscode(constant) and constant.co_name == name:

                        def get_index(attribute_name, _names=constant.co_names):
                            try:
                                return _names.index(attribute_name)
                            except ValueError:
                                return 0

                        break

                by_appearance = sorted(attributes.items(), key=lambda item: get_index(item[0]))
                for key, value in by_appearance:
                    namespace[key] = value

                return constructor(cls, name, bases, namespace)

            attributes['__new__'] = wraps(constructor)(preparing_constructor)
            return type.__new__(cls, name, bases, attributes)


class CatalogMeta(with_metaclass(Prepareable, type)):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        return OrderedDict()

    def __new__(metaname, clsname, bases, newattrs):
        kls = type.__new__(metaname, clsname, bases, newattrs)
        kls._member_map_ = OrderedDict()
        kls._member_names_ = []
        member_cls = newattrs.get('_member_class', CatalogMember)
        item_attrs = tuple(newattrs.get('_attrs', ['value']))
        kls._attrs_ = ('name', ) + item_attrs
        for attr, values in newattrs.items():
            if not attr.startswith('_'):
                kls._member_names_.append(attr)
                item = member_cls(attr, item_attrs, values)
                kls._member_map_[attr] = item
                setattr(kls, attr, item)

        return kls

    def __call__(cls, value, key=None):
        if key is None:
            key = cls._attrs_[1]
        return next((i for i in cls._member_map_.values() if getattr(i, key) == value), None)

    def __len__(cls):
        return len(cls._member_map_)

    def __iter__(cls):
        return (cls._member_map_[name] for name in cls._member_names_)

    def __reversed__(cls):
        return (cls._member_map_[name] for name in reversed(cls._member_names_))

    def __contains__(cls, member):
        return member in cls._member_map_.values()

    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError("cannot delete member '{}'".format(attr))
        super().__delattr__(attr)

    def _zip(cls, *attrs):
        if not attrs:
            attrs = cls._attrs_
        return (tuple(getattr(m, n) for n in attrs) for m in cls._member_map_.values())


class CatalogMember(object):

    def __init__(self, name, keys, values):
        if len(keys) == 1 and not isinstance(values, (list, tuple, set)):
            values = [
             values]
        for key, val in zip_longest(keys, values):
            if key:
                setattr(self, key, val)

        self.name = name

    def __repr__(self):
        return '<%s.%s: %r>' % (
         self.__class__.__name__, self.name, self.__dict__)

    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self.name)


class Catalog(with_metaclass(CatalogMeta, object)):
    __doc__ = "\n    Structure for complex enumeration\n\n    class Color(Catalog):\n        _attrs = 'value', 'label', 'other'\n        red = 1, 'Red', 'stuff'\n        blue = 2, 'Blue', 'things'\n\n    Access values as Attributes\n    Color.red.value -> 1\n    Color.red.label -> 'Red'\n\n    Call to look up members by attribute value\n    Color('Blue', 'label') -> Color.blue\n\n    Calling without attribute specified assumes first attribute defined in `_attrs`\n    Color(1) -> Color.red\n\n    `_attrs` defaults to `['value']`.\n    "