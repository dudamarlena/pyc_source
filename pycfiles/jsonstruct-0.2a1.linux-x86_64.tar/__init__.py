# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jsonstruct/__init__.py
# Compiled at: 2013-08-09 10:47:32
"""Python library for serializing any arbitrary object graph into JSON.

jsonstruct can take almost any Python object and turn the object into JSON.
Additionally, it can reconstitute the object back into Python.

The object must be accessible globally via a module and must
inherit from object (AKA new-style classes).

Create an object.

    >>> from jsonstruct._samples import Thing
    >>> obj = Thing('A String')
    >>> print obj.name
    A String

Use jsonstruct to transform the object into a JSON string.

    >>> import jsonstruct
    >>> pickled = jsonstruct.encode(obj)
    >>> print(pickled)
    {"py/object": "jsonstruct._samples.Thing", "name": "A String", "child": null}

Use jsonstruct to recreate a Python object from a JSON string

    >>> unpickled = jsonstruct.decode(pickled)
    >>> str(unpickled.name)
    'A String'

.. warning::

    Loading a JSON string from an untrusted source represents a potential
    security vulnerability.  jsonstruct makes no attempt to sanitize the input.

The new object has the same type and data, but essentially is now a copy of
the original.

    >>> obj == unpickled
    False
    >>> obj.name == unpickled.name
    True
    >>> type(obj) == type(unpickled)
    True

If you will never need to load (regenerate the Python class from JSON), you can
pass in the keyword unpicklable=False to prevent extra information from being
added to JSON.

    >>> oneway = jsonstruct.encode(obj, unpicklable=False)
    >>> print oneway
    {"name": "A String", "child": null}

"""
from jsonstruct.pickler import Pickler
from jsonstruct.unpickler import Unpickler
from jsonstruct.backend import JSONBackend
from jsonstruct.version import VERSION
__import__('jsonstruct._handlers')
__all__ = ('encode', 'decode')
__version__ = VERSION
json = JSONBackend()
set_preferred_backend = json.set_preferred_backend
set_encoder_options = json.set_encoder_options
load_backend = json.load_backend
remove_backend = json.remove_backend

def encode(value, max_depth=None, is_filter_none_attr=True):
    r"""
    Return a JSON formatted representation of value, a Python object.

    The keyword argument 'unpicklable' defaults to False.
    If set to False, the output will not contain the information
    necessary to turn the JSON data back into Python objects.

    The keyword argument 'max_depth' defaults to None.
    If set to a non-negative integer then jsonstruct will not recurse
    deeper than 'max_depth' steps into the object.  Anything deeper
    than 'max_depth' is represented using a Python repr() of the object.

    >>> encode('my string')
    '"my string"'
    >>> encode(36)
    '36'

    >>> encode({'foo': True})
    '{"foo": true}'

    >>> encode({'foo': True}, max_depth=0)
    '"{\'foo\': True}"'

    >>> encode({'foo': True}, max_depth=1)
    '{"foo": "True"}'

    """
    j = Pickler(unpicklable=False, max_depth=max_depth, is_filter_none_attr=is_filter_none_attr)
    return json.encode(j.flatten(value))


def decode(string, cls=None):
    """
    Convert a JSON string into a Python object.

    >>> str(decode('"my string"'))
    'my string'
    >>> decode('36')
    36
    """
    j = Unpickler()
    return j.restore(json.decode(string), cls)