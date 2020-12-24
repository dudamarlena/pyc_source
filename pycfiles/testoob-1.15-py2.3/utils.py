# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/utils.py
# Compiled at: 2009-10-07 18:08:46
"""General utilities used internally"""

def _pop(d, key, default):
    try:
        return d.pop(key, default)
    except AttributeError:
        pass

    try:
        return d.get(key, default)
    finally:
        if key in d:
            del d[key]


try:
    import cPickle as _pickle
except ImportError:
    import pickle as _pickle

def _is_pickleable(obj):
    """Is the object pickleable?"""
    try:
        _pickle.dumps(obj)
        return True
    except:
        return False


class UnpickleableFieldError(Exception):
    __module__ = __name__


def add_fields_pickling(klass, disable_unpickleable_fields=False):
    """
    Add pickling for 'fields' classes.

    A 'fields' class is a class who's methods all act as fields - accept no
    arguments and for a given class's state always return the same value.

    Useful for 'fields' classes that contain unpickleable members.

    Used in Testoob, http://code.google.com/p/testoob

    A contrived example for a 'fields' class:

      class Titles:
        def __init__(self, name):
          self.name = name
        def dr(self):
          return "Dr. " + self.name
        def mr(self):
          return "Mr. " + self.name

    If a method returns an unpickleable value there are two options:
    Default:
      Allow the instance to be pickled. If the method is called on the
      unpickled instance, an UnpickleableFieldError exception is raised.
      There is a possible performance concern here: each return value is
      pickled twice when pickling the instance.

    With disable_unpickleable_fields=True:
      Disallow pickling of instances with a method returning an unpickleable
      object.
    """

    def state_extractor(self):
        from types import MethodType
        fields_dict = {}
        unpickleable_fields = []

        def save_field(name, method):
            try:
                retval = method()
                if disable_unpickleable_fields or _is_pickleable(retval):
                    fields_dict[name] = retval
                else:
                    unpickleable_fields.append(name)
            except TypeError:
                raise TypeError('not a "fields" class, problem with method \'%s\'' % name)

        for attr_name in dir(self):
            if attr_name in ('__init__', '__getstate__', '__setstate__', '__getitem__', '__cmp__'):
                continue
            attr = getattr(self, attr_name)
            if type(attr) == MethodType:
                save_field(attr_name, attr)

        return (
         fields_dict, unpickleable_fields)

    def build_from_state(self, state):
        (fields_dict, unpickleable_fields) = state
        for name in fields_dict.keys():
            setattr(self, name, lambda name=name: fields_dict[name])

        for name in unpickleable_fields:

            def getter(name=name):
                raise UnpickleableFieldError("%s()'s result wasn't pickleable" % name)

            setattr(self, name, getter)

    klass.__getstate__ = state_extractor
    klass.__setstate__ = build_from_state