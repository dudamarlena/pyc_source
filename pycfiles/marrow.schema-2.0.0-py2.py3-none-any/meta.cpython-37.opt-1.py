# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/meta.py
# Compiled at: 2019-01-21 15:57:24
# Size of source mod 2**32: 4616 bytes
"""Marrow Schema metaclass definition.

This handles the irregularities of metaclass definition and usage across Python versions.
"""
from collections import OrderedDict as odict

class ElementMeta(type):
    __doc__ = "Instantiation order tracking and attribute naming / collection metaclass.\n\t\n\tTo use, construct subclasses of the Element class whose attributes are themselves instances of Element subclasses.\n\tFive attributes on your subclass have magical properties:\n\t\n\t* `inst.__sequence__`\n\t  An atomically incrementing (for the life of the process) counter used to preserve order.  Each instance of an\n\t  Element subclass is given a new sequence number automatically.\n\t  \n\t* `inst.__name__`\n\t  Element subclasses automatically associate attributes that are Element subclass instances with the name of the\n\t  attribute they were assigned to.\n\t  \n\t* `cls.__attributes__`\n\t  An ordered dictionary of all Element subclass instances assigned as attributes to your class. Class inheritance\n\t  of this attribute is handled differently: it is a combination of the `__attributes__` of all parent classes.\n\t  **Note:** This is only calculated at class construction time; this makes it efficient to consult frequently.\n\t  \n\t* `cls.__attributed__`\n\t  Called after class construction to allow you to easily perform additional work, post-annotation.\n\t  Should be a classmethod for full effect. Deprecatedi for many use cases; use Python's own `__init_subclass__`\n\t  instead. (This also allows arguments to be passed within the class definition, which is more flexible.)\n\t  \n\t* `cls.__fixup__`\n\t  If an instance of your Element subclass is assigned as a property to an Element subclass, this method of your\n\t  class will be called to notify you and allow you to make additional adjustments to the class using your subclass.\n\t  Should be a classmethod.\n\t\n\tGenerally you will want to use one of the helper classes provided (Container, Attribute, etc.) however this can be\n\tuseful if you only require extremely light-weight attribute features on custom objects.\n\t"
    sequence = 0

    def __new__(meta, name, bases, attrs):
        """Gather known attributes together, preserving order, and transfer attribute names to them."""
        if len(bases) == 1:
            if bases[0] is object:
                attrs['__attributes__'] = odict()
                return type.__new__(meta, str(name), bases, attrs)
        attributes = odict()
        overridden_sequence = dict()
        fixups = []
        for base in bases:
            if hasattr(base, '__attributes__'):
                attributes.update(base.__attributes__)

        for k in attrs:
            if k in attributes:
                overridden_sequence[k] = attributes[k].__sequence__
                attributes.pop(k, None)

        def process(name, attr):
            if not getattr(attr, '__name__', None):
                attr.__name__ = name
            if name in overridden_sequence:
                attr.__sequence__ = overridden_sequence[name]
            if hasattr(attr, '__fixup__'):
                fixups.append(attr)
            return (name, attr)

        attributes.update((process(k, v) for k, v in attrs.items() if isinstance(v, Element)))
        attrs['__attributes__'] = odict(sorted((attributes.items()), key=(lambda t: t[1].__sequence__)))
        cls = type.__new__(meta, str(name), bases, attrs)
        if hasattr(cls, '__attributed__'):
            cls.__attributed__()
        for obj in fixups:
            obj.__fixup__(cls)

        return cls

    def __call__(meta, *args, **kw):
        """Automatically give each new instance an atomically incrementing sequence number."""
        instance = (type.__call__)(meta, *args, **kw)
        instance.__sequence__ = ElementMeta.sequence
        ElementMeta.sequence += 1
        return instance


Element = ElementMeta('Element', (object,), dict())

class Element(metaclass=ElementMeta):
    pass