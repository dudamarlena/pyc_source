# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/registry.py
# Compiled at: 2017-07-20 07:37:33
# Size of source mod 2**32: 6940 bytes
__all__ = [
 'BaseRegistry',
 'PacketRegistry']
import threading
try:
    import bidict
except ImportError:
    HAVE_BIDICT = False
else:
    HAVE_BIDICT = True
from . import packet

class BaseRegistry(object):
    __doc__ = '\n    Basic registry class.\n    \n    Supports smart conversions between the integer, string and generic object representation of a registered entity.\n    \n    Optionally allows for automatic and threadsafe integer ID generation.\n    \n    Requires :py:mod:`bidict` to be installed and available.\n    \n    ``objtype`` may be used to override the class attribute of the same name per instance.\n    \n    Instances of this class also support dictionary-style access to their data,\n    e.g. ``reg[val]`` will always return the object representation of the value,\n    see :py:meth:`getObj()` for details.\n    '
    objtype = object

    def __init__(self, objtype=None):
        if not HAVE_BIDICT:
            raise RuntimeError('Bidict is required for usage of BaseRegistry')
        self.objtype = objtype if objtype is not None else self.objtype
        self.reg_int_obj = bidict.bidict()
        self.reg_int_str = bidict.bidict()
        self.nextid = 64
        self.idlock = threading.Lock()

    def getNewID(self):
        r"""
        Generates a new ID.
        
        Currently, all IDs are increasing from a fixed starting point, by default ``64``\ .
        """
        with self.idlock:
            n = self.nextid
            self.nextid += 1
            return n

    def register(self, obj, name, n=None):
        r"""
        Registers a relation between an object, its string representation and its integer representation.
        
        If ``n`` is not given, :py:meth:`getNewID()` will be used to generate it.
        
        Trying to register an already registered object may cause various kinds of corruptions on internal storages.
        
        Trying to register an object that is not of the type specified in :py:attr:`objtype` will result in an :py:exc:`TypeError`\ .
        """
        if not isinstance(obj, self.objtype):
            raise TypeError('This registry only accepts objects of type %s' % self.objtype)
        if n is None:
            n = self.getNewID()
        self.reg_int_obj[n] = obj
        self.reg_int_str[n] = name

    def registerObject(self, obj, n=None):
        r"""
        Same as :py:meth:`register()`\ , but extracts the string representation from the object's ``name`` attribute.
        """
        self.register(obj, obj.name, n)

    def deleteObj(self, obj):
        """
        Removes an object from the internal registry.
        
        ``obj`` may be any of the three representations of an object.
        """
        intid = self.getID(obj)
        del self.reg_int_obj[intid]
        del self.reg_int_str[intid]

    def getName(self, obj):
        r"""
        Converts the given value to its string representation.
        
        This method accepts either strings, integers or objects of type :py:attr:`objtype`\ .
        
        :py:meth:`getStr()` may be used as an alias to this method.
        """
        if isinstance(obj, str):
            return obj
        if isinstance(obj, int):
            return self.reg_int_str[obj]
        if isinstance(obj, self.objtype):
            return self.reg_int_str[self.reg_int_obj.inv[obj]]
        raise TypeError('Cannot convert object of type %s to name' % type(obj))

    getStr = getName

    def getID(self, obj):
        r"""
        Converts the given value to its integer representation.
        
        This method accepts either strings, integers or objects of type :py:attr:`objtype`\ .
        
        :py:meth:`getInt()` may be used as an alias to this method.
        """
        if isinstance(obj, int):
            return obj
        if isinstance(obj, str):
            return self.reg_int_str.inv[obj]
        if isinstance(obj, self.objtype):
            return self.reg_int_obj.inv[obj]
        raise TypeError('Cannot convert object of type %s to ID' % type(obj))

    getInt = getID

    def getObj(self, obj):
        r"""
        Converts the given value to its object representation.
        
        This method accepts either strings, integers or objects of type :py:attr:`objtype`\ .
        """
        if isinstance(obj, self.objtype):
            return obj
        if isinstance(obj, int):
            return self.reg_int_obj[obj]
        if isinstance(obj, str):
            return self.reg_int_obj[self.reg_int_str.inv[obj]]
        raise TypeError('Cannot convert object of type %s to Obj' % type(obj))

    def getAll(self, obj):
        r"""
        Returns a three-tuple of form ``(getObj(obj),getID(obj),getName(obj))``\ .
        """
        return (
         self.getObj(obj), self.getID(obj), self.getName(obj))

    def __getitem__(self, item):
        return self.getObj(item)


class PacketRegistry(BaseRegistry):
    __doc__ = '\n    Subclass of :py:class:`BaseRegistry` customized for storing :py:class:`~peng3dnet.packet.Packet` instances and instances of subclasses.\n    '
    objtype = packet.Packet