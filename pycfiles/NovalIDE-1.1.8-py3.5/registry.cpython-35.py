# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/registry.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 3508 bytes
try:
    from _winreg import *
except ImportError:
    from winreg import *

class Registry(object):
    __doc__ = 'description of class'

    def __init__(self, hkey=HKEY_CURRENT_USER):
        self._hkey = hkey

    @property
    def RootKey(self):
        return self._hkey

    def Open(self, subkey, access=KEY_READ):
        try:
            open_key = OpenKey(self.RootKey, subkey, 0, access)
        except Exception as e:
            return

        return Registry(open_key)

    def Exist(self, key):
        return self.Open(key) is not None

    def Read(self, value_name):
        return QueryValue(self.RootKey, value_name)

    def ReadEx(self, value_name):
        return QueryValueEx(self.RootKey, value_name)[0]

    def EnumChildKey(self):
        child_key_count = QueryInfoKey(self.RootKey)[0]
        for i in range(int(child_key_count)):
            name = EnumKey(self.RootKey, i)
            child_key = self.Open(name)
            yield child_key

    def EnumChildKeyNames(self):
        child_key_count = QueryInfoKey(self.RootKey)[0]
        for i in range(int(child_key_count)):
            name = EnumKey(self.RootKey, i)
            yield name

    def DeleteKey(self, key_name):
        DeleteKey(self.RootKey, key_name)

    def DeleteValue(self, value_name):
        DeleteValue(self.RootKey, value_name)

    def CreateKey(self, key_name):
        new_key = CreateKey(self.RootKey, key_name)
        return Registry(new_key)

    def WriteValue(self, key_name, value, val_type=REG_SZ):
        SetValue(self.RootKey, key_name, val_type, value)

    def WriteValueEx(self, value_name, value, val_type=REG_SZ):
        SetValueEx(self.RootKey, value_name, 0, val_type, value)

    def CreateKeys(self, key_str):
        keys = key_str.split('/')
        loop_key = None
        for key in keys:
            if loop_key is None:
                loop_key = self.CreateKey(key)
            else:
                loop_key = loop_key.CreateKey(key)

        return loop_key

    def DeleteKeys(self, key_str):
        key_path = key_str.replace('/', '\\')
        registry = self.Open(key_path)
        if registry is None:
            return
        names = list(registry.EnumChildKeyNames())
        if 0 == len(names):
            self.DeleteKey(key_path)
        else:
            for name in names:
                self.DeleteKeys(key_str + '/' + name)

            self.DeleteKeys(key_str)

    def CloseKey(self):
        CloseKey(self.RootKey)

    def __enter__(self):
        return self

    def __exit__(self, e_t, e_v, t_b):
        self.CloseKey()