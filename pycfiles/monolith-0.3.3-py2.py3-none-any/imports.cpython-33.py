# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/monolith/build/lib/monolith/utils/imports.py
# Compiled at: 2013-04-17 18:33:45
# Size of source mod 2**32: 935 bytes
import inspect

def import_class(class_path):
    """
    Returns class from the given path.

    For example, in order to get class located at
    ``mypackage.subpackage.MyClass``:

        try:
            hgrepo = import_class('mypackage.subpackage.MyClass')
        except ImportError:
            # hadle error
    """
    splitted = class_path.split('.')
    mod_path = '.'.join(splitted[:-1])
    class_name = splitted[(-1)]
    class_mod = __import__(mod_path, {}, {}, [class_name])
    try:
        cls = getattr(class_mod, class_name)
    except AttributeError:
        raise ImportError("Couldn't import %r" % class_path)

    return cls


def get_class(cls):
    """
    Returns given class. Can be given as a string - in that case proper class
    would be imported using ``import_class``.
    """
    if inspect.isclass(cls):
        return cls
    else:
        return import_class(cls)