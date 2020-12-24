# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pympris/Base.py
# Compiled at: 2013-12-10 15:49:59
__doc__ = "\nThis module provides a `Base` class used as a base class\nfor implementing MPRIS2 interfaces.\n\nDecorator 'signal_wrapper' used by `Base` class\nto convert function's arguments from dbus type to python type.\n\n`BaseMeta` metaclass (inherited ExceptionMeta and ConverterMeta classes)\nto avoid returning or raising dbus types and exceptions.\n"
from functools import partial, wraps
import types, dbus
from .common import convert, converter, exception_wrapper
IPROPERTIES = 'org.freedesktop.DBus.Properties'

def signal_wrapper(f):
    """Decorator converts function's arguments from dbus types to python."""

    @wraps(f)
    def wrapper(*args, **kwds):
        args = map(convert, args)
        kwds = {convert(k):convert(v) for k, v in kwds.items()}
        return f(*args, **kwds)

    return wrapper


class ExceptionMeta(type):
    """Metaclass wraps all class' functions and properties
    in `exception_wrapper` decorator to avoid raising dbus exceptions
    """

    def __new__(cls, name, parents, dct):
        fn = exception_wrapper
        for attr_name in dct:
            if isinstance(dct[attr_name], types.FunctionType):
                dct[attr_name] = fn(dct[attr_name])
            elif isinstance(dct[attr_name], property) and dct[attr_name].fget:
                dct[attr_name] = property(fn(dct[attr_name].fget) if dct[attr_name].fget else None, fn(dct[attr_name].fset) if dct[attr_name].fset else None, fn(dct[attr_name].fdel) if dct[attr_name].fdel else None)

        return super(ExceptionMeta, cls).__new__(cls, name, parents, dct)


class ConverterMeta(type):
    """Metaclass wraps all class' functions and properties
    in `converter` decorator to avoid returning dbus types
    """

    def __new__(cls, name, parents, dct):
        for attr_name in dct:
            if isinstance(dct[attr_name], types.FunctionType):
                dct[attr_name] = converter(dct[attr_name])
            elif isinstance(dct[attr_name], property) and dct[attr_name].fget:
                dct[attr_name] = property(converter(dct[attr_name].fget), dct[attr_name].fset, dct[attr_name].fdel)

        return super(ConverterMeta, cls).__new__(cls, name, parents, dct)


class BaseMeta(ExceptionMeta, ConverterMeta):
    pass


BaseVersionFix = BaseMeta('BaseVersionFix', (object,), {})

class Base(BaseVersionFix):
    """Base class provides common functionality
    for other classes which implement MPRIS2 interfaces"""
    OBJ_PATH = '/org/mpris/MediaPlayer2'

    def __init__(self, name, bus=None, private=False):
        """Init inner attributes to work with dbus.
        Parameters:
            name - unique or well-known objects name
            bus - bus object;
                  new SessionBus() object will be created if value is None.
            private - private connection (uses only if bus is None)

        below described attributes will be created:
            bus - Bus object from the functions argument or SessionBus()
            name - objects name from the functions argument
            proxy - DBUS proxy object
            iface - DBUS interface (uses self.IFACE path to create it)
            properties - DBUS interface to work with object's properties
            get - function to receive property's value
            set - function to set property's value
        """
        if not bus:
            bus = dbus.SessionBus(private=private)
        self.bus = bus
        self.name = name
        self.proxy = bus.get_object(name, self.OBJ_PATH)
        self.iface = dbus.Interface(self.proxy, self.IFACE)
        self.properties = dbus.Interface(self.proxy, IPROPERTIES)
        self.get = partial(self.properties.Get, self.IFACE)
        self.set = partial(self.properties.Set, self.IFACE)

    def register_signal_handler(self, signal_name, handler_function):
        """register `handler_function` to receive `signal_name`.

        Uses class's dbus interface self.IFACE, objects name self.name
            and objects path self.OBJ_PATH to match signal.
        """
        self.bus.add_signal_receiver(signal_wrapper(handler_function), signal_name=signal_name, dbus_interface=self.IFACE, bus_name=self.name, path=self.OBJ_PATH)