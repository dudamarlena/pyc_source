# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\base.py
# Compiled at: 2017-04-06 15:23:44
# Size of source mod 2**32: 1856 bytes
"""
Similar to ``collections.namedtuple``, ``nameddict`` is a data container class.

**中文文档**

和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法
对属性, 值进行for循环, 以及和list, dict之间的IO交互。
"""
try:
    from .pkg import nameddict, name_convention
except:
    from constant.pkg import nameddict, name_convention

SEP = '____'

class Base(nameddict.Base):
    __doc__ = 'nameddict base class.\n    '
    __attrs__ = None

    def items(self):
        return [(key, value) for key, value in super(Base, self).items() if SEP not in key]

    def _getattr_by_key_value(self, key):
        """High order function for self.getattr_by_field(value).
        """

        def getattr_by_key_value(value):
            return getattr(self, '%s____%s' % (key, name_convention.to_index_key(value)))

        return getattr_by_key_value

    def __getattr__(self, attr):
        """  

        >>> obj.getattr_by_name("John") == obj.name____John
        >>> True

        >>> obj.name____John.name == "John"
        >>> True
        """
        if attr.startswith('getattr_by_'):
            key = attr.replace('getattr_by_', '')
            return self._getattr_by_key_value(key)
        else:
            return object.__getattribute__(self, attr)


if __name__ == '__main__':
    pass