# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\pyjld\trunk\pyjld.system\trunk\src\pyjld\system\registry\base.py
# Compiled at: 2009-04-02 21:58:17
__doc__ = ' \npyjld.system.registry.base\n'
__author__ = 'Jean-Lou Dupont'
__fileid = '$Id: base.py 37 2009-04-03 01:58:16Z jeanlou.dupont $'
__all__ = [
 'Registry', 'RegistryException']
import sys

class RegistryException(Exception):
    """ 
    An exception class for Registry
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Registry(object):
    """
    Facade for the cross-platform Registry
    
    Can be accessed like a dictionary: for this
    functionality, an instance must be constructed
    with the 'file' parameter specified.
    """
    reg = None

    def __init__(self, file=None):
        self.file = file
        if sys.platform[:3] == 'win':
            from pyjld.system.registry.reg_windows import WindowsRegistry
            self.reg = WindowsRegistry(file)
        else:
            from pyjld.system.registry.reg_linux import LinuxRegistry
            self.reg = LinuxRegistry(file)

    def getKey(self, file, key):
        """
        GETS the specified key
        """
        return self.reg.getKey(file, key)

    def setKey(self, file, key, value, cond=False):
        """
        SETS the specified key
        """
        if cond:
            if value is None:
                return
        return self.reg.setKey(file, key, value)

    def __getitem__(self, key):
        return self.reg.get(key, None)

    def __setitem__(self, key, value):
        self.reg[key] = value

    def __contains__(self, key):
        return key in self.reg