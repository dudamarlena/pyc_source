# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycurry\__init__.py
# Compiled at: 2009-10-25 04:27:46
__doc__ = 'General utilities for the pycurry package.\n\nCopyright (c) 2008 Fons Dijkstra\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n'
import re, os, sys, inspect

def pass_():
    """A 'do-nothing' function. Can for example be used for storing a function
    pointer that does nothing by default.

    ensure: __return__ is None
    """
    pass


def fully_qualified_name(typ, cls=None):
    """The fully qualified name of the provided type as a string.

    The provided type must be module, function, class or method. When a
    method is still a function, in a meta-class implementation for example, 
    one can provide the defining class explicitely.

    ensure: isinstance(__return__, str)
    """
    if inspect.ismodule(typ):
        result = typ.__name__
    elif inspect.isfunction(typ):
        if cls is None:
            result = '%s.%s' % (typ.__module__, typ.__name__)
        else:
            result = '%s.%s' % (fully_qualified_name(cls), typ.__name__)
    elif inspect.isclass(typ):
        result = '%s.%s' % (typ.__module__, typ.__name__)
    elif inspect.ismethod(typ):
        result = '%s.%s' % (fully_qualified_name(typ.im_class), typ.__name__)
    else:
        raise TypeError('unknown type: %s' % type(typ))
    return result


def source_filename(name):
    """Retrieve the python source-file name, so without any optional trailing
    'c' or 'o'.

    require: isinstance(name, str)
    ensure: __return__ is None or isinstance(__return__, str)
    """
    rgx = re.match('(?P<name>.+\\.py)(c|o)?', name)
    if rgx is None:
        return
    else:
        return rgx.group('name')


def resolve_filename(name, path=sys.path):
    """
    Utility function to join the supplied name with a certain search path to an 
    absolute path. By default the system search path is used.

    require: isinstance(name, str)
    require: isinstance(path, collection.Iterable)
    require: not [p for p in path if not isinstance(p, str)]
    ensure: not __return__ or isinstance(__return__, str)
    ensure: not __return__ or os.path.isabs(__return__)
    ensure: not __return__ or os.path.exists(__return__)
    """
    if not os.path.isabs(name):
        for p in path:
            if os.path.isabs(p):
                result = os.path.join(p, name)
                if os.path.exists(result):
                    break
        else:
            result = None
    elif os.path.exists(name):
        result = name
    else:
        result = None
    if result is not None:
        result = os.path.normpath(result)
    return result


def generic_repr(obj):
    """Generic implementation for __repr__ methods. The type of the provided
    object together with its attributes are flattened.

    ensure: isinstance(__return__, str)
    """
    if not hasattr(obj, '__dict__'):
        raise TypeError('must be an object: %s' % type(obj))
    return '%r: %r' % (type(obj), obj.__dict__)


def generic_str(obj):
    """Generic implementation for __str__ methods. The type and identification
    of the provided object together with, as readable as possible, its
    attributes are flattened.

    ensure: isinstance(__return__, str)
    """
    if not hasattr(obj, '__dict__') or not hasattr(obj, '__class__'):
        raise TypeError('must be an object: %s' % type(obj))
    result = '%s(0x%08X)' % (obj.__class__.__name__, id(obj))
    for (index, (name, attr)) in enumerate(obj.__dict__.iteritems()):
        if index == 0:
            result += ': '
        else:
            result += '; '
        reg = re.match('^_{1}\\w+_{2}(?P<name>\\w+)$', name)
        if reg is not None:
            name = reg.group('name')
        result += '%s=%s' % (name, attr)

    return result