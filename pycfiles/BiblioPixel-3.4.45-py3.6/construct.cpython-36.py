# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/construct.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1746 bytes
import copy
from . import aliases, importer, load

def construct(*args, datatype, typename=None, **kwds):
    """
    Construct an object from a type constructor.

    A type constructor is a dictionary which has a field "datatype" which has
    a callable method to construct a class, and a field "typename" which is the
    Python path of the function or class in "datatype".
    """
    return datatype(*args, **kwds)


def to_type(d):
    fn = load.load_if_filename(d)
    if fn:
        return fn
    if isinstance(d, str):
        return {'typename': d}
    else:
        result = copy.deepcopy(d)
        if 'datatype' in result:
            result.pop('typename', None)
        return result


def to_type_constructor(value, python_path=None):
    """"
    Tries to convert a value to a type constructor.

    If value is a string, then it used as the "typename" field.

    If the "typename" field exists, the symbol for that name is imported and
    added to the type constructor as a field "datatype".

    Throws:
         ImportError -- if "typename" is set but cannot be imported
         ValueError -- if "typename" is malformed
    """
    if not value:
        return value
    else:
        if callable(value):
            return {'datatype': value}
        value = to_type(value)
        typename = value.get('typename')
        if typename:
            r = aliases.resolve(typename)
            try:
                value['datatype'] = importer.import_symbol(r,
                  python_path=python_path)
                del value['typename']
            except Exception as e:
                value['_exception'] = e

        return value


def construct_type(desc, python_path=None):
    tc = to_type_constructor(desc, python_path)
    return construct(**tc)