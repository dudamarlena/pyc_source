# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pympris/common.py
# Compiled at: 2013-12-10 15:49:59
__doc__ = '\nThis module provides helper functions:\n\n`convert2dbus` - converts from Python type to DBUS type according signature\n`convert` - function to convert dbus object to python object.\n`converter` - decorator to convert dbus object to python object.\n`exception_wrapper` - decorator to convert dbus exception to pympris exception.\n`available_players` - function searchs and returns unique names of objects\n                      which implemented MPRIS2 interfaces.\n\n'
import sys
from functools import wraps, partial
from collections import namedtuple
import dbus
PY3 = sys.version_info[0] == 3
MPRIS_NAME_PREFIX = 'org.mpris.MediaPlayer2'

def convert2dbus(value, signature):
    """Convert Python type to dbus type according signature"""
    if len(signature) == 2 and signature.startswith('a'):
        return dbus.Array(value, signature=signature[(-1)])
    dbus_string_type = dbus.String if PY3 else dbus.UTF8String
    type_map = {'b': dbus.Boolean, 
       'y': dbus.Byte, 'n': dbus.Int16, 'i': dbus.Int32, 
       'x': dbus.Int64, 'q': dbus.UInt16, 'u': dbus.UInt32, 't': dbus.UInt64, 
       'd': dbus.Double, 'o': dbus.ObjectPath, 'g': dbus.Signature, 
       's': dbus_string_type}
    return type_map[signature](value)


def convert(dbus_obj):
    """Convert dbus_obj from dbus type to python type"""
    _isinstance = partial(isinstance, dbus_obj)
    ConvertType = namedtuple('ConvertType', 'pytype dbustypes')
    pyint = ConvertType(int, (dbus.Byte, dbus.Int16, dbus.Int32, dbus.Int64,
     dbus.UInt16, dbus.UInt32, dbus.UInt64))
    pybool = ConvertType(bool, (dbus.Boolean,))
    pyfloat = ConvertType(float, (dbus.Double,))
    pylist = ConvertType(lambda _obj: list(map(convert, dbus_obj)), (
     dbus.Array,))
    pytuple = ConvertType(lambda _obj: tuple(map(convert, dbus_obj)), (
     dbus.Struct,))
    types_str = (dbus.ObjectPath, dbus.Signature, dbus.String)
    if not PY3:
        types_str += (dbus.UTF8String,)
    pystr = ConvertType(str if PY3 else unicode, types_str)
    pydict = ConvertType(lambda _obj: dict(zip(map(convert, dbus_obj.keys()), map(convert, dbus_obj.values()))), (
     dbus.Dictionary,))
    for conv in (pyint, pybool, pyfloat, pylist, pytuple, pystr, pydict):
        if any(map(_isinstance, conv.dbustypes)):
            return conv.pytype(dbus_obj)
    else:
        return dbus_obj


def converter(f):
    """Decorator to convert from dbus type to Python type"""

    @wraps(f)
    def wrapper(*args, **kwds):
        return convert(f(*args, **kwds))

    return wrapper


def exception_wrapper(f):
    """Decorator to convert dbus exception to pympris exception"""

    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except dbus.exceptions.DBusException as err:
            _args = err.args
            raise PyMPRISException(*_args)

    return wrapper


def available_players():
    """Search and return set of unique names of objects
    which implemented MPRIS2 interfaces."""
    bus = dbus.SessionBus()
    players = set()
    for name in filter(lambda item: item.startswith(MPRIS_NAME_PREFIX), bus.list_names()):
        owner_name = bus.get_name_owner(name)
        players.add(convert(owner_name))

    return players


class PyMPRISException(Exception):
    """docstring for PyMPRISException"""

    def __init__(self, *args):
        super(PyMPRISException, self).__init__(*args)