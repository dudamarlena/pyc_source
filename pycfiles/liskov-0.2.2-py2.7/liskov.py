# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/liskov/liskov.py
# Compiled at: 2013-10-05 17:22:13
__all__ = [
 'behave_as', 'can_substitute', 'subtype', 'append_sys_path', 'constrain', 'under_constraint']

def behave_as(*bases):
    substitute_bases = _load_bases(bases)

    class Liskov(type):
        constraints = tuple()

        def __new__(cls, name, bases, attrs):
            new_bases = _remove_bases_behaviours(substitute_bases, cls.constraints)
            return type.__new__(cls, name, new_bases + bases, attrs)

        @classmethod
        def except_for(cls, *behaviours):
            cls.constraints = behaviours
            return cls

    return Liskov


def subtype(base):
    mod_name, sep, cls_name = base.rpartition('.')
    module = __import__(mod_name, globals(), locals(), [cls_name])
    return getattr(module, cls_name)


def can_substitute(*bases):
    substitute_bases = _load_bases(bases)

    def liskov(cls, substitute_bases=substitute_bases):
        if hasattr(cls, 'constrained_subtype'):
            substitute_bases = _remove_bases_behaviours(substitute_bases, cls.constrained_subtype)
        bases = (cls,) + substitute_bases + cls.__bases__
        attrs = dict(cls.__dict__)
        attrs['substitute_bases'] = substitute_bases
        return type(cls.__name__, bases, attrs)

    return liskov


def under_constraint(*behaviours):

    def constraints(cls):
        setattr(cls, 'constrained_subtype', behaviours)
        return cls

    return constraints


class constrain(object):

    def __init__(self, *behaviours):
        self.constraints = behaviours

    def __rand__(self, cls):
        bases = _remove_bases_behaviours(cls.__bases__, self.constraints)
        attrs = _remove_behaviours(cls.__dict__, self.constraints)
        return type(cls.__name__, bases, attrs)

    __ror__ = __radd__ = __rsub__ = __rand__


def append_sys_path(path):
    import sys, os
    if os.path.isfile(path):
        path = os.path.dirname(path)
    sys.path.append(os.path.realpath(path))


def _remove_bases_behaviours(bases, behaviours):
    new_bases = tuple()
    for base in bases:
        base_attrs = base.__dict__
        attrs = _remove_behaviours(base_attrs, behaviours)
        if len(base_attrs) > len(attrs):
            base = type(base.__name__, base.__bases__, attrs)
        new_bases += (base,)

    return new_bases


def _remove_behaviours(attrs, behaviours):
    new_attrs = dict()
    for key, value in list(attrs.items()):
        if key not in behaviours:
            new_attrs[key] = value

    return new_attrs


def _load_bases(bases):
    substitute_bases = tuple()
    for base in bases:
        cls = subtype(base)
        if cls not in substitute_bases:
            substitute_bases += (cls,)

    return substitute_bases