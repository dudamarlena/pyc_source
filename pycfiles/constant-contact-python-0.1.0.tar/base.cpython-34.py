# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\base.py
# Compiled at: 2017-04-06 15:23:44
# Size of source mod 2**32: 1856 bytes
__doc__ = '\nSimilar to ``collections.namedtuple``, ``nameddict`` is a data container class.\n\n**中文文档**\n\n和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法\n对属性, 值进行for循环, 以及和list, dict之间的IO交互。\n'
try:
    from .pkg import nameddict, name_convention
except:
    from constant.pkg import nameddict, name_convention

SEP = '____'

class Base(nameddict.Base):
    """Base"""
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